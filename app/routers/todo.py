from fastapi import APIRouter

# Arguments to pass to todo_router
TODO_ROUTER_CONFIGURATION = {
    'prefix': "/todo",
    'tags': ["Todo"]
}

# Route for all todo related endpoints
todo_router = APIRouter(**TODO_ROUTER_CONFIGURATION)

# ----------------------- Routing starts here -----------------------
@todo_router.get('/')
def todo_root():
    return {'message': 'You are at todo root!!'}