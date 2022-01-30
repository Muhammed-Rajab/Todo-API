from app.core import auth as auth_core
from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import UserInDB, UserLogin, UserRegister, UserResponse
from app.crud.auth import create_new_user

# Arguments to pass to todo_router
AUTH_ROUTER_CONFIGURATION = {
    'prefix': "/auth",
    'tags': ["Authentication"],
}

# Route for all todo related endpoints
auth_router = APIRouter(**AUTH_ROUTER_CONFIGURATION)

@auth_router.post('/register/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register_user(new_user: UserRegister):
    return create_new_user(new_user)



"""
{
  "first_name": "Jake",
  "last_name": "Paul",
  "email": "jpaulstar98@outlook.com",
  "password": "thisisjakepaulyo_1",
  "confirm_password": "thisisjakepaulyo_1"
}
"""