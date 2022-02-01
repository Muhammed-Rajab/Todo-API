from datetime import datetime
from enum import Enum
from time import time
from pydantic import BaseModel, Field
from app.schemas.base import ObjectId, BSONObjectID

# Enum to store priority values
class TodoPriorityEnum(int, Enum):
    low = 1
    low_med = 2
    med = 3
    high_med = 4
    high = 5

# Class representation of todo from database
class TodoInDB(BaseModel):
    
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    index: int
    title: str
    body: str
    added: datetime
    edited: bool = False
    finished: bool = False
    user__id: ObjectId
    priority: TodoPriorityEnum = TodoPriorityEnum.low

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
    finished: bool = False
    priority: TodoPriorityEnum = TodoPriorityEnum.low

class TodoCreate(BaseTodo):
    priority: TodoPriorityEnum = TodoPriorityEnum.low

class TodoUpdate(BaseTodo):
    finished: bool = False
    priority: TodoPriorityEnum = TodoPriorityEnum.low