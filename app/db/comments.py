from app.db import mongo 

async def instert_comments(comments: list[dict]):
    if not comments or mongo.db is None:
        return
    await mongo.db.comments.insert_many(comments)