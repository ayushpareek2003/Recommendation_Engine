from fastapi import FastAPI,Query
from dotenv import load_dotenv
from typing import Optional
import requests
import os
load_dotenv()
from fastapi import FastAPI
from pymongo import MongoClient
from app.infer import Graph_infer 
from app.infer import Neural_Graph_infer
from app.db_setup import user_migration
from app.services import get_post
app = FastAPI()

from motor.motor_asyncio import AsyncIOMotorClient


client = MongoClient("mongodb://localhost:27017")
db = client["test"]  
collection_user = db["user_data"]  
collection_post=db["post"]

@app.get("/health")
def root():
    return {"message": "healthy"}


@app.get("/feed")
def get_feed(
    user_name: str = Query(..., description="User ID"),  
    project_code: Optional[str] = Query(None, description="Category or project code")  
):
    user_id=collection_user.find_one({"username":user_name}).get("user_id")
    posts_graph = Graph_infer.recommend_posts(user_id,20)
    if project_code is None:
        res=get_post.pull(posts_graph)
        return res
    
    project_code_posts = Neural_Graph_infer.rank_posts(posts_graph,project_code)
    res=get_post.pull(project_code_posts)
    return res


####### data migration happening through herre #############
@app.get("/get_users")
async def get_one_document():
    flic_token = os.getenv("FLIC_TOKEN")
    headers = {
        "Flic-Token": flic_token
    }
    urls = {
        "users": os.getenv("GET_ALL_USERS_URL"),
        "viewed": os.getenv("POST_VIEW_URL"),
        "liked": os.getenv("POST_LIKED_URL"),
        "inspired": os.getenv("POST_INSPIRED_URL"),
        "rated": os.getenv("USER_RATED_URL"),
        "summary": os.getenv("POST_DATA_URL"),
    }

    # Fetch data
    user_response = requests.get(urls["users"], headers=headers)
    post_view_response = requests.get(urls["viewed"], headers=headers)
    post_liked_response = requests.get(urls["liked"], headers=headers)
    post_inspired_response = requests.get(urls["inspired"], headers=headers)
    user_rated_response = requests.get(urls["rated"], headers=headers)
    post_data_response = requests.get(urls["summary"], headers=headers)

    if post_data_response.status_code == 200:
        result = collection_post.insert_many(post_data_response.json().get("posts",[])) 
        
        
    if user_response.status_code == 200:
        data = user_response.json()
        users = data.get("users", [])
        viewed_post = post_view_response.json().get("posts", [])
        liked_post = post_liked_response.json().get("posts", [])
        inspired_post = post_inspired_response.json().get("posts", [])
        rated_post = user_rated_response.json().get("posts", [])

        if not users:
            return {"message": "No users to migrate."}

        # Prepare users for insertion into MongoDB
        
        user_documents= user_migration.fill_user_table(users,liked_post,viewed_post,inspired_post,rated_post)
        try:
            if user_documents:
                result = collection_user.insert_many(user_documents)
                print(f"Inserted {len(result.inserted_ids)} users")
                return {"message":"migration done "}
            else:
                return {"message": "No users to migrate."}
        except Exception as e:
            print(f"Error inserting data: {e}")
            return {"message": f"Error inserting data: {str(e)}"}

    else:
        return {"message": f"Failed to fetch data. Status Code: {user_response.status_code}"}
    
