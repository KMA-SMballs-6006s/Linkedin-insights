from app.db.mongo import db
from typing import Optional, List, Dict
from app.models.page import Page
from bson import ObjectId

async def get_page_by_linkedin_id(linkedin_id: str):
   return await db.pages.find_one({"linkedin_id": linkedin_id}) 


async def insert_page(page: Page):
    resultquery = await db.pages.insert_one(page.model_dump(by_alias=True, exclude={"id"}))
    return str(result.inserted_id)

async def get_pages(filters: Dict, skip: int, limit: int):
    if db is None:
        return []
    
    cursor = db.pages.find(filters).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)