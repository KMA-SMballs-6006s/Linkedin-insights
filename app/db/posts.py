from app.db import mongo

async def get_posts_by_page_paginated(page_id: str, skip: int, limit: int):
    if mongo.db.posts is None:
        return []
    
    cursor = mongo.db.posts.find({"page_id": page_id}).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)
