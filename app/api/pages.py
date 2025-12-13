from fastapi import APIRouter, HTTPException, Query
from app.db.pages import get_page_by_linkedin_id, insert_page
from app.db.posts import get_posts_by_page_paginated
from app.services.scraper import scrape_linkedin_page
from app.models.page import Page
from typing import Optional
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
    
@router.get("/pages/")
async def list_pages(
    min_followeres: Optional[int] = Query(None),
    max_followeres: Optional[int] = Query(None),
    industry: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    page: int = Query(1, ge=1),
):
    filters = {}

    if min_followeres is not None or max_followeres is not None:
        filters["followers"] = {}
        if min_followeres is not None:
            filters["followers"]["$gte"] = min_followeres
        if max_followeres is not None:
            filters["followers"]["$lte"] = max_followeres

    if industry:
        filters["industry"] = industry

    if search:
        filters["name"] = {"$regex": search, "$options": "i"}

    skip = (page - 1) * limit

    pages = await get_pages(filters=filters, skip=skip, limit=limit)
    return{
        "page": page,
        "limit": limit,
        "pages": pages
    }

@router.get("/pages/{page_id}/posts")
async def get_page_posts(
    page_id: str,
    limit: int = Query(10, ge=1, le=50),
    page: int = Query(1, ge=1),
):
    skip = (page - 1) * limit
    
    posts = await get_posts_by_page_paginated(
        page_id=page_id, 
        skip=skip, 
        limit=limit,
    )

    return {
        "page": page,
        "limit": limit,
        "posts": posts
    }