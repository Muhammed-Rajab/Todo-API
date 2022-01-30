from app.core import auth as auth_core
from fastapi import APIRouter, HTTPException, status
from app.crud.auth import check_user_exists, create_new_user
from app.schemas.auth import UserInDB, UserLogin, UserRegister

# Arguments to pass to todo_router
AUTH_ROUTER_CONFIGURATION = {
    'prefix': "/auth",
    'tags': ["Authentication"],
}

# Route for all todo related endpoints
auth_router = APIRouter(**AUTH_ROUTER_CONFIGURATION)