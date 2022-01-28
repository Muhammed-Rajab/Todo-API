from datetime import datetime
from time import time
from pydantic import BaseModel, Field
from app.schemas.base import ObjectId, BSONObjectID

# Class representation of todo from database
class TodoInDB(BaseModel):
    
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    index: int
    title: str
    body: str
    added: datetime
    edited: bool = False

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {BSONObjectID: str}

# --------------------------- Schemas ---------------------------
class BaseTodo(BaseModel):
    title: str
    body: str

class Todo(BaseTodo):
    index: int
    added: datetime
    edited: bool = False

class TodoCreate(BaseTodo):
    ...

class TodoUpdate(BaseTodo):
    ...