from typing import Sequence
from app.schemas.todo import TodoInDB
from fastapi import HTTPException, status
from app.database.db_init import todo_db as db

todos_collection = db['Todo']

def get_todos(limit: int = 1) -> Sequence[TodoInDB]:
    return list(map(lambda todo: TodoInDB(**todo), todos_collection.find().limit(limit)))

def get_todo_by_index(index: int) -> TodoInDB:
    res = todos_collection.find_one({'index': index})
    if res:
        return TodoInDB(**res)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo of index {index} not found")