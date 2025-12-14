from fastapi import APIRouter
from app.db import mongo

router = APIRouter()

@router.get("/posts/{post_id}/comments")
async def list_comments(post_id: str):
    if mongo.db is None:
        return []
    
    cursor = mongo.db.comments.find({"post_id": post_id})
    return await cursor.to_list(length=100)