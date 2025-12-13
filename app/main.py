from fastapi import FastAPI

app = FastAPI(title="LinkedIn Insights ")

@app.get("/")
def health ():
    return {"status": "ok"}