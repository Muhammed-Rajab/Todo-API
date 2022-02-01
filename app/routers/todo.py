from app.schemas.auth import Token
from app.crud.todo import TodoCRUD
from typing import Optional, Sequence
from app.dependencies.deps import get_current_token
from fastapi import APIRouter, Depends, Query, Path
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
def get_todos(limit: Optional[int] =  Query(10, gt=0, description="Limit of todos to fetch."), token: Token =  Depends(get_current_token)):
    """
        Returns todos according to the limit.
    """
    return TodoCRUD().get_todos(token=token, limit=limit)

@todo_router.get('/{index}', response_model=Todo)
def fetch_todo_by_index(index: int = Path(..., description="Index of todo to fetch", gt=0), token: Token =  Depends(get_current_token)):
    """
        Returns todo of specified index
    """
    return TodoCRUD().get_todo_by_index(token=token, index=index)

@todo_router.post('/create', response_model=Todo)
def create_todo(new_todo: TodoCreate, token: Token =  Depends(get_current_token)):
    """
        Creates a new todo
    """
    return TodoCRUD().create_new_todo(token=token, new_todo=new_todo)

@todo_router.put('/{index}', response_model=Todo)
def update_todo(index: int, updated_todo: TodoUpdate, token: Token =  Depends(get_current_token)):
    """
        Updates a todo of specific index
    """
    return TodoCRUD().update_existing_todo(token=token, index=index, updated_todo=updated_todo)

@todo_router.delete('/{index}', status_code=204)
def delete_todo(index: int, token: Token =  Depends(get_current_token)):
    """
        Deletes a todo of specific index
    """
    TodoCRUD.delete_todo(token=token, index=index)