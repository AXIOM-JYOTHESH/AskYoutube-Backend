import logging
import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.api import router

logger = logging.getLogger(__name__)

if not os.environ.get("PINECONE_API_KEY"):
    logger.warning("PINECONE_API_KEY is not set or empty. Please set it in your .env file.")


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Running 🚀"}