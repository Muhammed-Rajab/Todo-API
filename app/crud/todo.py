from typing import Sequence
from datetime import datetime
from pymongo import ReturnDocument
from fastapi import HTTPException, Response, status
from app.database.db_init import todos_collection
from app.schemas.auth import Token
from app.schemas.todo import Todo, TodoInDB, TodoCreate, TodoUpdate

def get_todos(token: Token, limit: int = 1) -> Sequence[TodoInDB]:
    print(token)
    return list(map(lambda todo: TodoInDB(**todo), todos_collection.find().limit(limit)))

def get_todo_by_index(token: Token, index: int) -> TodoInDB:
    res = todos_collection.find_one({'index': index})
    if res:
        return TodoInDB(**res)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo of index {index} not found")

def create_new_todo(token: Token, new_todo: TodoCreate) -> TodoInDB:
    time = datetime.now()
    try:
        index = list(todos_collection.find().sort('age', -1))[0]['index'] + 1
    except:
        index = 1
    todo = TodoInDB(index=index, **new_todo.dict(), added=time)
    todos_collection.insert_one(todo.dict(by_alias=True))
    return todo

def update_existing_todo(token: Token, index: int, updated_todo: TodoUpdate) -> TodoInDB:

    updated_todo_dict = updated_todo.dict()
    updated_todo_dict['edited'] = True

    existing_todo = todos_collection.find_one_and_update({'index':index}, {'$set':updated_todo_dict}, return_document=ReturnDocument.AFTER)
    
    if not existing_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo of index {index} not found")

    return existing_todo

def delete_todo(token: Token, index: int) -> TodoInDB:
    deleted = todos_collection.find_one_and_delete({'index': index})
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo of index {index} not found")
    return TodoInDB(**deleted)