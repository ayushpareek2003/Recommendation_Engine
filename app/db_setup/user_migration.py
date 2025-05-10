
def assign_posts_to_users(post_list, field_name, mode="simple"):
    count=0
    for post in post_list:
        user_id = post.get("user_id")
        post_id = post.get("post_id")

        if user_id not in user_id_to_doc:
            # Create a dummy user document for unknown user
            dummy_user = {
                "user_id": user_id,
                "first_name": "Unknown",
                "last_name": "",
                "username": f"user_{user_id}",
                "gender": "unknown",
                "role": "unknown",
                "user_type": "unknown",
                "post_count": 0,
                "liked_posts": [],
                "viewed_posts": [],
                "rated_posts": [],
                "inspired_posts": [],
            }
            user_id_to_doc[user_id] = dummy_user
            user_documents.append(dummy_user)

        
        if mode == "simple":
            
            user_id_to_doc[user_id][field_name].append(post_id)

        elif mode == "rating":
            rating_entry = {
                 "post_id": int(post.get("post_id")),
                "rating_percent": int(post.get("rating_percent", 0))
            }
            user_id_to_doc[user_id][field_name].append(rating_entry)



def fill_user_table(users,liked_post,viewed_post,inspired_post,rated_post):
    # Prepare users for insertion into MongoDB
    global user_id_to_doc
    user_id_to_doc = {}
    global user_documents
    user_documents= []

    for user in users:
        user_doc = {
                "user_id": user.get("id"),
                "first_name": user.get("first_name"),
                "last_name": user.get("last_name"),
                "username": user.get("username"),
                "gender": user.get("gender"),
                "role": user.get("role"),
                "user_type": user.get("user_type"),
                "post_count": user.get("post_count"),
                "liked_posts": [],
                "viewed_posts": [],
                "rated_posts": [],
                "inspired_posts": [],
            }

        user_id_to_doc[user["id"]] = user_doc
        user_documents.append(user_doc)

        # Assign post interactions
    assign_posts_to_users(liked_post, "liked_posts", mode="simple")
    assign_posts_to_users(viewed_post, "viewed_posts", mode="simple")
    assign_posts_to_users(inspired_post, "inspired_posts", mode="simple")
    assign_posts_to_users(rated_post, "rated_posts", mode="rating")

    return user_documents




