from dotenv import load_dotenv
load_dotenv()
import os
while(os.environ.get("PINECONE_API_KEY") == ''):
    continue
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.api import router

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