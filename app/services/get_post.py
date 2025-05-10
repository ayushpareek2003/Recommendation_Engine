
from pymongo import MongoClient
from typing import Union, List

client = MongoClient("mongodb://localhost:27017/")
db = client["test"]
collection_posts = db["post"]


def pull(posts: Union[int, List[int]]):
    query_fields = {
        "_id": 0,  # exclude MongoDB's _id field
        "id": 1,
        "title": 1,
        "video_link": 1,
        "username": 1,
        "upvote_count": 1
    }

    if isinstance(posts, int):
        post = collection_posts.find_one({"id": posts}, query_fields)
        return post or {}
    elif isinstance(posts, list):
        print("hi")
        return list(collection_posts.find({"id": {"$in": posts}}, query_fields))
    else:
        return {}
    

# if __name__=="__main__":
#     out=pull([78,15,25])
    
