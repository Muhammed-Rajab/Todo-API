from typing import Sequence
from datetime import datetime
from app.schemas.auth import Token
from pymongo import ReturnDocument
from app.schemas.base import ObjectId
from fastapi import HTTPException, status
from app.database.db_init import todos_collection
from app.schemas.todo import TodoInDB, TodoCreate, TodoUpdate

class TodoCRUD:

    def _get_many_todos(self, limit: int, **keys) -> Sequence[TodoInDB]:
        # Fetches and converts all todo dict to TodoInDB 
        # with given user__id from token
        cursor = todos_collection.find(keys).limit(limit)
        return list(map(lambda todo: TodoInDB(**todo), cursor))
    
    def _get_one_todo(self, **keys) -> TodoInDB:
        res = todos_collection.find_one(keys)
        if res:
            return TodoInDB(**res)
        return None
    
    def _get_last_index(self, user__id: ObjectId) -> int:
        
        try:
            # Gets index of latest todo
            index = list(todos_collection.find({'user__id': user__id}).sort('index', -1))[0]['index']
            return index
        except:
            # If there is no todo, returns 0 so that it can be incremented before creating new todo
            return 0
        

    def get_todos(self, token: Token, limit: int = 1) -> Sequence[TodoInDB]:
        return self._get_many_todos(
            limit=limit, 
            user__id=ObjectId(token.sub))

    def get_todo_by_index(self, token: Token, index: int) -> TodoInDB:
        
        res = self._get_one_todo(index=index, user__id=ObjectId(token.sub))
        
        if res: return res

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo of index {index} not found")

    def create_new_todo(self, token: Token, new_todo: TodoCreate) -> TodoInDB:
        
        time = datetime.now()
        index = self._get_last_index(user__id=ObjectId(token.sub)) + 1

        todo = TodoInDB(
            index=index, **new_todo.dict(), 
            added=time, user__id=ObjectId(token.sub)
        )

        todos_collection.insert_one(todo.dict(by_alias=True))
        
        return todo

    def update_existing_todo(self, token: Token, index: int, updated_todo: TodoUpdate) -> TodoInDB:

        updated_todo_dict = updated_todo.dict()
        updated_todo_dict['edited'] = True

        existing_todo = todos_collection.find_one_and_update(
            {
                'index':index, 
                'user__id': ObjectId(token.sub)
            }, 
            {
                '$set':updated_todo_dict},
            return_document=ReturnDocument.AFTER
        )
    
        if not existing_todo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo of index {index} not found")

        return existing_todo

    def delete_todo(token: Token, index: int) -> TodoInDB:
        
        deleted = todos_collection.find_one_and_delete(
            {
                'index': index, 
                'user__id': ObjectId(token.sub)
            }
        )
        
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo of index {index} not found")
        
        return TodoInDB(**deleted)