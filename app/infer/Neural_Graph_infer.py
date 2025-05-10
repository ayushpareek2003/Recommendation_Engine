import re
from sentence_transformers import SentenceTransformer, util
import numpy as np
from pymongo import MongoClient

model = SentenceTransformer("BAAI/bge-base-en-v1.5")
client = MongoClient("mongodb://localhost:27017/")
db = client["test"]
users_col = db["post"]

def get_concise_description(description: str) -> str:
    paragraphs = description.strip().split("\n\n")
    first = paragraphs[0] if paragraphs else ""

    def extract_section(title):
        match = re.search(rf'### {title}\n(.+?)(\n###|$)', description, re.DOTALL)
        return match.group(1).strip() if match else ""

    theme = extract_section("Theme and Message")
    narrative = extract_section("Narrative Flow")

    return f"{first} | Theme: {theme} | Narrative: {narrative}"
def extend_path(path, post):
    val = post
    for key in path:
        if isinstance(val, dict):
            val = val.get(key, {})
        elif isinstance(val, list):
            val = [item.get(key, '') for item in val if isinstance(item, dict)]
            val = " ".join(val)
        else:
            val = ""
    return val if isinstance(val, str) else str(val)

def flatten_post(post_id):
    post = users_col.find_one({"id": post_id})
    if not post:
        return ""
    
    summary = post.get("post_summary", {})
    title = post.get("title", "Untitled")
    description = get_concise_description(summary.get("description", ""))

    parts = [f"Title: {title}", description]

    meta_paths = [
        ("actions", "main_actions"),
        ("audio_elements", "specifics"),
        ("emotions", "primary_emotions"),
        ("psycological_view_of_video", "traits"),
        ("topics_of_video", "theme"),
        ("topics_of_video", "visual_storytelling"),
        ("topics_of_video", "emotional_conflicts"),
        ("targeted_audiance", "groups"),
        ("visual_elements_of_video", "notable_features"),
        ("quality_indicators", "marks"),
    ]

    for path in meta_paths:
        parts.append(extend_path(path, summary))  # note: summary, not post

    for kw in summary.get("keywords", []):
        parts.append(f"{kw.get('keyword', '')}")

    return " | ".join(filter(None, parts))

def rank_posts(posts, query, top_k=20):
    post_texts = [flatten_post(p) for p in posts]
 
    query_embedding = model.encode(query, convert_to_tensor=True)
    post_embeddings = model.encode(post_texts, convert_to_tensor=True)
  

    similarities = util.pytorch_cos_sim(query_embedding, post_embeddings)[0]
    # return similarities
    top_indices = np.argsort(-similarities.cpu().numpy())[:top_k]


    return [posts[i] for i in top_indices]


# if __name__=="__main__":
#     hol=[1066,724,82,658,169]
#     ans=rank_posts(hol,"trials")
#     for post_id, _ in ans:
#         post = users_col.find_one({"id": post_id})
#         if post:
#             print(post.get("id"))
    

    


