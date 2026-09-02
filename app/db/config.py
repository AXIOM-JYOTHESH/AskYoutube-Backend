from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

client = MongoClient(os.environ.get("MONGO_URI"), server_api=ServerApi('1'))
db = client["youtube_rag"]
collection = db["videos"]