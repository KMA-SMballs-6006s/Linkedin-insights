# 📊 LinkedIn Insights API

A backend service that fetches and serves insights about public LinkedIn company pages using a scrape-on-demand approach with persistence, caching, and pagination.

This project demonstrates backend system design, async APIs, external data ingestion, and defensive engineering practices.

## 🧩 Problem Summary

LinkedIn exposes limited public data for company pages and does not provide an open API for structured access.

**Goal:**
Build a backend service that:
* Fetches public company data from LinkedIn
* Stores it for reuse
* Exposes clean, paginated APIs
* Handles scraping failures gracefully
* Avoids unnecessary repeated scraping

The system must work without login, without crashing, and with partial data allowed.

## 🏗 Architecture Overview

```text
Client (curl / browser / Swagger)
        |
        v
   FastAPI Application
        |
        |-- In-memory Cache (TTL = 5 min)
        |
        |-- MongoDB (persistent storage)
        |
        |-- Playwright Scraper (fallback)
              |
              v
        LinkedIn Public Pages
````

**Flow for `/pages/{page_id}`**

1.  Check in-memory cache
2.  If miss → check MongoDB
3.  If not found → scrape LinkedIn
4.  Store result in DB
5.  Cache response
6.  Return JSON response

## 📡 API Endpoints

### Health Check

`GET /health`

**Response:**

```json
{ "status": "ok" }
```

### Fetch a LinkedIn Page (Core Endpoint)

`GET /pages/{page_id}`

**Example:**
`GET /pages/microsoft`

**Response:**

```json
{
  "_id": "66c9f2a1e3b7c0f9a1234567",
  "linkedin_id": "microsoft",
  "name": "Microsoft",
  "linkedin_url": "[https://www.linkedin.com/company/microsoft/](https://www.linkedin.com/company/microsoft/)",
  "industry": "Software"
}
```

**Behavior:**

  * First request may scrape.
  * Subsequent requests are cached.
  * Returns `404` if scraping fails.

### List Pages (Filters + Pagination)

`GET /pages`

**Query Parameters:**

  * `search` — partial name match
  * `industry` — exact match
  * `limit` — results per page (default 10)
  * `page` — page number (default 1)

**Example:**
`GET /pages?search=micro&limit=5&page=1`

### List Posts for a Page

`GET /pages/{page_id}/posts`

**Example:**
`GET /pages/microsoft/posts?limit=3&page=1`

Returns paginated posts (may be empty if not yet stored).

### AI Summary (Stub)

`GET /pages/{page_id}/summary`

**Response:**

```json
{
  "page_id": "microsoft",
  "summary": "AI-generated summary will be available here in a future version."
}
```

*This is a documented placeholder to show extensibility.*

## 🕷 Scraping Details & Limitations

  * **Tool:** Uses Playwright (headless Chromium).
  * **Target:** Scrapes public LinkedIn company pages only.
  * **Auth:** No authentication or cookies used.
  * **Best-effort extraction:**
      * Partial data is acceptable.
      * Missing fields return `null`.
  * **Failure Strategy:**
      * If LinkedIn blocks or layout changes, the scraper returns `None`.
      * API responds with `404` (no crash).

> **Important:** This project prioritizes stability over completeness.

## ⚙️ How to Run Locally

### 1️⃣ Prerequisites

  * Python 3.11+
  * MongoDB running locally
  * Windows / Linux / macOS

### 2️⃣ Clone & Setup

```bash
git clone <repo-url>
cd linkedin-insights
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate # Mac/Linux
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 4️⃣ Environment Variables

Create a `.env` file in the root directory:

```env
MONGO_URI=mongodb://localhost:27017
DB_NAME=linkedin_insights
```

### 5️⃣ Run Server (Important)

```bash
uvicorn app.main:app
```

> ⚠️ **Note:** On Windows, do not use `--reload` when scraping (Playwright limitation).

### 6️⃣ Test

  * **Health:** `curl http://127.0.0.1:8000/health`
  * **Fetch:** `curl http://127.0.0.1:8000/pages/microsoft`
  * **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## ⚖️ Trade-offs & Design Decisions

**Why scrape instead of API?**

  * LinkedIn has no public API for this data.
  * Scraping is the only viable approach for public info.

**Why in-memory cache?**

  * Simple and fast.
  * No external dependencies (like Redis) required for setup.
  * Acceptable for demo/assignment scope.

**Why best-effort scraping?**

  * HTML changes frequently.
  * Reliability \> Completeness.
  * System must not crash on partial failures.

**Why no background jobs?**

  * Keep architecture minimal.
  * Avoid premature complexity.
  * Scrape only when needed.

## 🚀 Future Improvements (Out of Scope)

  * [ ] Normalize followers count to integers
  * [ ] Background scraping for posts
  * [ ] Redis cache
  * [ ] MongoDB indexes
  * [ ] Rate limiting
  * [ ] Real AI summaries

## ✅ Assignment Status

  - [x] Core endpoint implemented
  - [x] Async architecture
  - [x] Database persistence
  - [x] Scrape fallback
  - [x] Pagination & filters
  - [x] Caching with TTL
  - [x] Defensive error handling
  - [x] Clear documentation
