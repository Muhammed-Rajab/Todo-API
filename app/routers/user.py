from app.dependencies import deps
from app.crud.auth import UserCRUD
from fastapi import APIRouter, Depends
from app.schemas.auth import Token, User


USER_ROUTER_CONFIGURATION = {
    'prefix': "/user",
    'tags': ["User"]
}


# Route to take care of logged user related stuff
user_router = APIRouter(**USER_ROUTER_CONFIGURATION)

@user_router.get("/me", response_model=User)
def get_logged_user(current_user: User = Depends(deps.get_current_user)):
    # Returns the currently logged user from token in the header
    return current_user

@user_router.delete("/delete")
def delete_logged_user(token: Token = Depends(deps.get_current_token)):
    return UserCRUD().delete(token=token)
