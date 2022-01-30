from app.dependencies import deps
from app.core import auth as auth_core
from app.crud.auth import create_new_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.auth import User, UserInDB, UserLogin, UserRegister, UserResponse, TokenResponse

# Arguments to pass to todo_router
AUTH_ROUTER_CONFIGURATION = {
    'prefix': "/auth",
    'tags': ["Authentication"],
}

# Route for all todo related endpoints
auth_router = APIRouter(**AUTH_ROUTER_CONFIGURATION)

token_handler = auth_core.TokenHandler()

@auth_router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register_user(new_user: UserRegister):
    return create_new_user(new_user)

@auth_router.post('/login', status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
def login_user(login_data: OAuth2PasswordRequestForm = Depends()):

    user = auth_core.authenticate(email=login_data.username,  password=login_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    
    token = token_handler.signJWT(sub = str(user.id))
    return TokenResponse(access_token=token)

@auth_router.get("/me", response_model=User)
def get_logged_user(current_user: User = Depends(deps.get_current_user)):
    return current_user
"""
{
  "first_name": "Jake",
  "last_name": "Paul",
  "email": "jpaulstar98@outlook.com",
  "password": "thisisjakepaulyo_1",
  "confirm_password": "thisisjakepaulyo_1"
}
"""