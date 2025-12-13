import logging
from typing import Optional, Dict, Any, List
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

async def scrape_linkedin_page(page_id: str) -> Optional[Dict[str, Any]]:
    url = f"https://www.linkedin.com/company/{page_id}/"

    data: Dict[str, Any] = {}

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            await page.goto(url, timeout=60000)
            await page.wait_for_timeout(3000)

            try:
                data["name"] = await page.locator("h1").first.inner_text()
            except Exception:
                data["name"] = None

            try:
                data["description"] = await page.locator("section.aboutus-us__descrn").inner_text()
            except Exception:
                data["description"] = None
            
            try:
                followers_text = await page.locator("span.org-top-card-summary__following-count").inner_text()
                data["followers"] = followers_text
            except Exception:
                data["followers"] = None

            try:
                data["industry"] = await page.locator("dd.org-page-details__defination-text").nth(0).inner_text()
            except Exception:
                data["industry"] = None
            
            try:
                data["profile_pic"] = await page.locator("img.org-top-card-primary-content__logo").get_attribute("src")
            except Exception:
                data["profile_pic"] = None
            
            try:
                data["website"] = await page.locator("a.org-page-details__defination-link").first.get_attribute("herf")
            except Exception:
                data["website"] = None


            posts: List[Dict[str, Any]] = []
            cards = page.locator("div.feed-shared-update-v2")
            count = min(await cards.count(), 15)

            for i in range(count):
                try:
                    text = await cards.nth(i).locator("p").inner_text()
                    posts.append({"text": text})
                except Exception:
                    continue

            data["posts"] = posts

            await browser.close()
            return data
        
    except Exception as e:
        logging.error(f"Failed to scrape LinkedIn page {page_id}: {e}")
        return None