from fastapi import APIRouter, HTTPException
from app.db.pages import get_page_by_linkedin_id, insert_page
from app.services.scraper import scrape_linkedin_page
from app.models.page import Page
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/pages/{page_id}")
async def get_page(page_id: str):
    page = await get_page_by_linkedin_id(page_id)
    if page:
        return page
    
    scraped = await scrape_linkedin_page(page_id)
    if not scraped:
        raise HTTPException(status_code=404, detail="Page not found")
    
    try:
        page_model= Page(
            name=scraped.get("name"),
            linkedin_url=f"https://www.linkedin.com/company/{page_id}/",
            industry=scraped.get("industry"),
        )

        inserted_id = await insert_page(page_model)
        page_model.id = inserted_id

        return page_model
    
    except Exception as e:
        logger.error(f"failed to store scraped page{page_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")