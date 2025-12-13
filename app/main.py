from fastapi import FastAPI
from app.db.mongo import connect_to_mongo, close_mongo_connection
from app.api.pages import router as pages_router

app = FastAPI(title="LinkedIn Insights API")

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

app.include_router(pages_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}