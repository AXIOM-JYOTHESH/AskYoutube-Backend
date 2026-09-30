import logging
import os
from dotenv import load_dotenv

load_dotenv()

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.routes.api import router

logger = logging.getLogger(__name__)

if not os.environ.get("PINECONE_API_KEY"):
    logger.warning("PINECONE_API_KEY is not set or empty. Please set it in your .env file.")


app = FastAPI(title="AskYoutube AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

STATIC_DIR = Path(__file__).parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", response_class=HTMLResponse)
def root():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>AskYoutube AI Backend Running 🚀</h1>")