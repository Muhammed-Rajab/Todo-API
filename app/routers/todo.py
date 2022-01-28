from app.crud import todo
from app.schemas.todo import Todo
from typing import Optional, Sequence
from fastapi import APIRouter, Query, Path

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