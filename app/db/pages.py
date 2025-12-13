from app.db import mongo
from typing import Optional, List, Dict
from app.models.page import Page
from bson import ObjectId

async def get_page_by_linkedin_id(linkedin_id: str):
   if mongo.db is None:
       return None
   
   return await mongo.db.pages.find_one({"linkedin_id": linkedin_id}) 

async def insert_page(page: Page):
    resultquery = await mongo.db.pages.insert_one(page.model_dump(by_alias=True, exclude={"id"}))
    return str(result.inserted_id)

async def get_pages(filters: Dict, skip: int, limit: int):
    if mongo.db is None:
        return []
    
    cursor = mongo.db.pages.find(filters).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)