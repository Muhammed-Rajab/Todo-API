# from typing import Generator
from pymongo import MongoClient
from app.core.config import  settings

"""
def get_mongo_client() -> Generator:
    client = MongoClient(settings.MONGODB_URL)
    try:
        yield client    
    finally:
        client.close()
"""
client = MongoClient(settings.MONGODB_URL)