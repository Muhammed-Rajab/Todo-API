import json
from app.crud import todo
from typing import Optional, Sequence
from fastapi import APIRouter, Query, Path, Response
from app.schemas.todo import Todo, TodoCreate, TodoUpdate

# Arguments to pass to todo_router
TODO_ROUTER_CONFIGURATION = {
    'prefix': "/todo",
    'tags': ["Todo"]
}

# Route for all todo related endpoints
todo_router = APIRouter(**TODO_ROUTER_CONFIGURATION)

# ----------------------- Routing starts here -----------------------
@todo_router.get('/get', response_model=Sequence[Todo])
def get_todos(
    limit: Optional[int] =  Query(10, gt=0, description="Limit of todos to fetch.")):
    """
        Returns todos according to the limit.
    """
    return todo.get_todos(limit)

@todo_router.get('/{index}', response_model=Todo)
def fetch_todo_by_index(index: int = Path(..., description="Index of todo to fetch", gt=0)):
    """
        Returns todo of specified index
    """
    return todo.get_todo_by_index(index)

@todo_router.post('/create', response_model=Todo)
def create_todo(new_todo: TodoCreate):
    """
        Updates a todo of specific index
    """
    return todo.create_new_todo(new_todo)

@todo_router.put('/{index}', response_model=Todo)
def update_todo(index: int, updated_todo: TodoUpdate):
    return todo.update_existing_todo(index, updated_todo)

@todo_router.delete('/{index}', status_code=204)
def delete_todo(index: int):
    todo.delete_todo(index)