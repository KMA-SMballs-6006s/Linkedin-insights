from app.db.mongo import db

async def get_posts_by_page_paginated(page_id: str, skip: int, limit: int):
    if db is None:
        return []
    
    cursor = db.posts.find({"page_id": page_id}).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)
