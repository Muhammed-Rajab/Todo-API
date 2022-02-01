from app.dependencies import deps
from app.crud.auth import UserCRUD
from app.core import auth as auth_core
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.auth import User, UserRegister, UserResponse, TokenResponse

# Arguments to pass to todo_router
AUTH_ROUTER_CONFIGURATION = {
    'prefix': "/auth",
    'tags': ["Authentication"],
}

# Route for all todo related endpoints
auth_router = APIRouter(**AUTH_ROUTER_CONFIGURATION)

# Token handler to decode and encode JWT tokens
token_handler = auth_core.TokenHandler()

@auth_router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register_user(new_user: UserRegister):
    return UserCRUD().create(new_user)

@auth_router.post('/login', status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
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

@auth_router.get("/me", response_model=User)
def get_logged_user(current_user: User = Depends(deps.get_current_user)):
    # Returns the currently logged user from token in the header
    return current_user