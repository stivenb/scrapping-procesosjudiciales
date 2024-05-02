import uvicorn
from fastapi import FastAPI

from app.routers import web_scraping

app = FastAPI(title="API Fapro", version="0.1.0")

@app.get("/api/v1/greetings")
async def root():
    return "Scraping procesos judiciales"

app.include_router(web_scraping.router)

# if __name__ == "__main__":
#     uvicorn.run("main:app", port=8000, reload=True)