import pickle
from pymongo import MongoClient
from collections import Counter


with open("D:\\intern_sub\\fastapi\\app\\user_graph.pkl", "rb") as f:
    G = pickle.load(f)


client = MongoClient("mongodb://localhost:27017/")
db = client["test"]
users_col = db["user_data"]

def recommend_posts(user_id,top_k_similar_users=10, top_k_posts=30):
    if user_id not in G:
        print(f"[!] User {user_id} not found in graph.")
        return []


    neighbors = sorted(G[user_id].items(), key=lambda x: x[1]['weight'], reverse=True)
    top_users = [n for n, _ in neighbors[:top_k_similar_users]]


    user_doc = users_col.find_one({"user_id": user_id})
    if not user_doc:
        print(f"[!] User {user_id} not found in database.")
        return []

    seen_posts = set(
        user_doc.get("liked_posts", []) +
        user_doc.get("viewed_posts", []) +
        user_doc.get("inspired_posts", []) +
        [r["post_id"] for r in user_doc.get("rated_posts", [])]
    )

    post_scores = Counter()

    for uid in top_users:
        neighbor_doc = users_col.find_one({"user_id": uid})
        if not neighbor_doc:
            continue

        posts = neighbor_doc.get("liked_posts", []) + \
                neighbor_doc.get("viewed_posts", []) + \
                neighbor_doc.get("inspired_posts", []) + \
                [r["post_id"] for r in neighbor_doc.get("rated_posts", [])]

        for post_id in posts:
            if post_id not in seen_posts:
                post_scores[post_id] += 1  


    recommended = [post for post, _ in post_scores.most_common(top_k_posts)]
    return recommended


