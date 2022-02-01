# from typing import Generator
from pymongo import MongoClient
from app.core.config import  settings

client = MongoClient(settings.MONGODB_URL)

todo_db = client['TodoAPI']

todos_collection = todo_db['Todo']
user_collection = todo_db['User']