from pymongo import MongoClient
import networkx as nx
from collections import defaultdict
from itertools import combinations
import pickle

client = MongoClient("mongodb://localhost:27017/")
db = client["test"]
users_col = db["user_data"]


INTERACTION_WEIGHTS = {
    "like": 3,
    "view": 1,
    "inspired": 4,
}

post_user_weight = defaultdict(lambda: defaultdict(float))
all_user_ids = set()

for user_doc in users_col.find():
    user_id = user_doc.get("user_id")
    if not user_id:
        continue
    all_user_ids.add(user_id)

    # Like
    for post_id in user_doc.get("liked_posts", []):
        post_user_weight[post_id][user_id] += INTERACTION_WEIGHTS["like"]

    # View
    for post_id in user_doc.get("viewed_posts", []):
        post_user_weight[post_id][user_id] += INTERACTION_WEIGHTS["view"]

    # Inspired
    for post_id in user_doc.get("inspired_posts", []):
        post_user_weight[post_id][user_id] += INTERACTION_WEIGHTS["inspired"]

  
    for rating in user_doc.get("rated_posts", []):
        post_id = rating.get("post_id")
        score = rating.get("score", 0)  
        post_user_weight[post_id][user_id] += (score / 5.0) * 5 


G = nx.Graph()
for uid in all_user_ids:
    G.add_node(uid)


for post_id, user_weights in post_user_weight.items():
    users = list(user_weights.keys())
    for u1, u2 in combinations(users, 2):
        weight_u1 = user_weights[u1]
        weight_u2 = user_weights[u2]
        shared_weight = min(weight_u1, weight_u2) 

        if G.has_edge(u1, u2):
            G[u1][u2]["weight"] += shared_weight
        else:
            G.add_edge(u1, u2, weight=shared_weight)


print(f"Total users in DB: {users_col.count_documents({})}")
print(f"Total users in graph: {G.number_of_nodes()} (including isolated)")
print(f"Total user-user edges: {G.number_of_edges()}")
