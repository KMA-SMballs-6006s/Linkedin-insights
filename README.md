# 📊 LinkedIn Insights API

A backend service that fetches and serves insights about **public LinkedIn company pages** using a scrape-on-demand approach with persistence, caching, and pagination.

This project focuses on **backend system design**, **async APIs**, **external data ingestion**, and **defensive engineering** rather than perfect data accuracy.

---

## 🧩 Problem Summary

LinkedIn does not provide a public API for accessing structured company page data.  
However, some information is publicly visible on company pages.

### Objective

Build a backend service that:

- Fetches public LinkedIn company data
- Stores results for reuse
- Avoids repeated scraping
- Exposes clean, paginated APIs
- Handles failures gracefully
- Works without authentication or login

The system must **never crash**, even if scraping fails or returns partial data.

---

## 🏗 Architecture Overview

```

Client (Browser / curl / Swagger)
|
v
FastAPI Application
|
|-- In-Memory Cache (TTL = 5 minutes)
|
|-- MongoDB (Persistent Storage)
|
|-- Playwright Scraper (Fallback)
|
v
LinkedIn Public Company Pages

```

### Core Request Flow (`GET /pages/{page_id}`)

1. Check in-memory cache  
2. If cache miss → check MongoDB  
3. If not found → scrape LinkedIn  
4. Persist result in MongoDB  
5. Cache the response  
6. Return normalized JSON  

---

## 📡 API Endpoints

### Health Check

```

GET /health

````

Response:
```json
{ "status": "ok" }
````

---

### Fetch a LinkedIn Page (Core Endpoint)

```
GET /pages/{page_id}
```

Example:

```
GET /pages/microsoft
```

Response:

```json
{
  "_id": "66c9f2a1e3b7c0f9a1234567",
  "linkedin_id": "microsoft",
  "name": "Microsoft",
  "linkedin_url": "https://www.linkedin.com/company/microsoft/",
  "industry": "Software"
}
```

Behavior:

* First request may trigger scraping
* Subsequent requests are served from cache or DB
* Returns `404` if scraping fails

---

### List Pages (Filters + Pagination)

```
GET /pages
```

Query Parameters:

* `search` — partial name match
* `industry` — exact match
* `limit` — results per page (default: 10)
* `page` — page number (default: 1)

Example:

```
GET /pages?search=micro&limit=5&page=1
```

---

### List Posts for a Page

```
GET /pages/{page_id}/posts
```

Example:

```
GET /pages/microsoft/posts?limit=3&page=1
```

Returns paginated posts.
If no posts are stored yet, an empty list is returned.

---

### AI Summary (Stub)

```
GET /pages/{page_id}/summary
```

Response:

```json
{
  "page_id": "microsoft",
  "summary": "AI-generated summary will be available here ."
}
```

> This endpoint is a documented placeholder to demonstrate extensibility.

---

## 🕷 Scraping Details & Limitations

* Uses **Playwright (headless Chromium)**
* Scrapes **public LinkedIn company pages only**
* No login, cookies, or authentication
* Best-effort extraction:

  * Partial data is acceptable
  * Missing fields return `null`
* If LinkedIn blocks scraping or layout changes:

  * Scraper returns `None`
  * API responds with `404`
  * Application does not crash

**Design priority:**
Reliability and graceful degradation over data completeness.

---

## ⚙️ How to Run Locally

### 1️⃣ Prerequisites

* Python 3.11+
* MongoDB running locally
* Windows / Linux / macOS

---

### 2️⃣ Clone & Setup

```bash
git clone <repository-url>
cd linkedin-insights
python -m venv .venv
.venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

---

### 4️⃣ Environment Variables

Create a `.env` file in the project root:

```env
MONGO_URI=mongodb://localhost:27017
DB_NAME=linkedin_insights
```

---

### 5️⃣ Run the Server

```bash
uvicorn app.main:app
```

> ⚠️ On Windows, avoid using `--reload` when scraping due to Playwright subprocess limitations.

---

### 6️⃣ Test

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/pages/microsoft
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 🐳 Docker Support (Optional)

Docker is provided as a **deployment-ready option**.
Local development is still recommended using `uvicorn`.

### Build Image

```bash
docker build -t linkedin-insights .
```

### Run Container

```bash
docker run -p 8000:8000 --env-file .env linkedin-insights
```

API will be available at:

```
http://127.0.0.1:8000
```

### Docker Notes

* MongoDB runs **outside** the container
* On Windows / macOS, use:

```env
MONGO_URI=mongodb://host.docker.internal:27017
```

---

## ⚖️ Trade-offs & Design Decisions

### Why scraping instead of an API?

* LinkedIn does not offer a public API for this data
* Scraping is the only viable approach for public information

### Why in-memory cache?

* Simple and fast
* No external dependency
* Sufficient for assignment scope

### Why best-effort scraping?

* HTML changes frequently
* Stability is more important than completeness
* The system must not crash due to external changes

### Why no background jobs?

* Keeps architecture simple
* Avoids premature complexity
* Scraping occurs only when data is requested

---

## 🚀 Future Improvements (Out of Scope)

* Normalize follower counts to integers
* Background scraping for posts
* Redis-based caching
* MongoDB indexing
* Rate limiting
* Real AI-generated summaries

---

## ✅ Assignment Status

* ✔ Core endpoint implemented
* ✔ Async FastAPI architecture
* ✔ MongoDB persistence
* ✔ Scrape fallback
* ✔ Pagination & filters
* ✔ In-memory caching with TTL
* ✔ Defensive error handling
* ✔ Docker support
* ✔ Clear documentation

---