from typing import Sequence
from datetime import datetime
from pymongo import ReturnDocument
from fastapi import HTTPException, Response, status
from app.database.db_init import todo_db as db
from app.schemas.todo import Todo, TodoInDB, TodoCreate, TodoUpdate

todos_collection = db['Todo']

def get_todos(limit: int = 1) -> Sequence[TodoInDB]:
    return list(map(lambda todo: TodoInDB(**todo), todos_collection.find().limit(limit)))

def get_todo_by_index(index: int) -> TodoInDB:
    res = todos_collection.find_one({'index': index})
    if res:
        return TodoInDB(**res)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo of index {index} not found")

def create_new_todo(new_todo: TodoCreate) -> TodoInDB:
    time = datetime.now()
    try:
        index = list(todos_collection.find().sort('age', -1))[0]['index'] + 1
    except:
        index = 1
    todo = TodoInDB(index=index, **new_todo.dict(), added=time)
    todos_collection.insert_one(todo.dict(by_alias=True))
    return todo

def update_existing_todo(index: int, updated_todo: TodoUpdate) -> TodoInDB:

    updated_todo_dict = updated_todo.dict()
    updated_todo_dict['edited'] = True

    existing_todo = todos_collection.find_one_and_update({'index':index}, {'$set':updated_todo_dict}, return_document=ReturnDocument.AFTER)
    
    if not existing_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo of index {index} not found")

    return existing_todo

def delete_todo(index: int) -> TodoInDB:
    deleted = todos_collection.find_one_and_delete({'index': index})
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo of index {index} not found")
    return TodoInDB(**deleted)