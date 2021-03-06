from typing import Optional
from app.dependencies import deps
from app.crud.auth import UserCRUD
from app.core import auth as auth_core
from app.routers.user import user_router
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import (
    APIRouter,
    File, 
    HTTPException,
    UploadFile, 
    status, 
    Depends,
)
from app.schemas.auth import Token, User, UserRegister, UserRegisterForm, UserResponse, TokenResponse

# Arguments to pass to todo_router
AUTH_ROUTER_CONFIGURATION = {
    'prefix': "/auth"
}

# Route for all todo related endpoints
auth_router = APIRouter(**AUTH_ROUTER_CONFIGURATION)

# Token handler to decode and encode JWT tokens
token_handler = auth_core.TokenHandler()

"""
    Leaving this code in case if the current solution
    breaks.
"""
# @auth_router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse, tags=["Authentication"])
# def register_user(
#     first_name: str = Form(..., max_length=30),
#     last_name: str = Form(..., max_length=30),
#     email: str = Form(..., max_length=255),
#     password: str = Form(..., min_length=8),
#     confirm_password: str = Form(..., min_length=8)
#     ):
#     new_user = UserRegister(
#         first_name=first_name,
#         last_name=last_name,
#         email=email,
#         password=password,
#         confirm_password=confirm_password
#     )
#     return UserCRUD().create(new_user)

@auth_router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse, tags=["Authentication"])
async def register_user(
    new_user: UserRegisterForm = Depends(),
    profile_picture: Optional[UploadFile] = None
    ):
    
    profile_picture_file_bytes = None

    if profile_picture:
        profile_picture_file_bytes = await profile_picture.read()
        print(len(profile_picture_file_bytes))

    return UserCRUD().create(UserRegister(**new_user.dict()), profile_picture=profile_picture_file_bytes)

@auth_router.post('/login', status_code=status.HTTP_201_CREATED, response_model=TokenResponse, tags=["Authentication"])
def login_user(login_data: OAuth2PasswordRequestForm = Depends()):

    # Checks whether the login credentials are valid or not
    # If valid returns user else False
    user = auth_core.authenticate(email=login_data.username,  password=login_data.password)

    # If user credentials aren't valid
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    
    # Creates a JWT token
    token = token_handler.signJWT(sub = str(user.id))
    return TokenResponse(access_token=token)

auth_router.include_router(user_router)