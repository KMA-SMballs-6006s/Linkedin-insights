from app.db.mongo import db

async def get_posts_by_post(page_id: str):
    cursor = db.posts.find({"page_id": page_id})
    return await cursor.to_list(length=100)
