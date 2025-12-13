from app.db.mongo import db
from app.models.page import Page
from bson import ObjectId

async def get_page_by_id(page_id: str):
    return await db.pages.find_one({"_id": ObjectId(page_id)})


async def insert_page(page: Page):
    resultquery = await db.pages.insert_one(page.model_dump(by_alias=True, exclude={"id"}))
    return str(result.inserted_id)
