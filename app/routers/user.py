from app.dependencies import deps
from app.crud.auth import UserCRUD
from app.schemas.auth import Token, User, UserUpdateForm
from fastapi import APIRouter, Depends, UploadFile, status


USER_ROUTER_CONFIGURATION = {
    'prefix': "/user",
    'tags': ["User"]
}


# Route to take care of logged user related stuff
user_router = APIRouter(**USER_ROUTER_CONFIGURATION)

@user_router.get("/me", response_model=User)
def get_logged_user(token: Token = Depends(deps.get_current_token)):
    # Returns the currently logged user details from token in the header
    return UserCRUD().get_current_user_details(token=token)

@user_router.delete("/delete")
def delete_logged_user(token: Token = Depends(deps.get_current_token)):
    return UserCRUD().delete(token=token)

@user_router.put("/update", response_model=User)
def update_user_details(token: Token = Depends(deps.get_current_token), updated_user_details: UserUpdateForm = Depends()):
    return UserCRUD().update_user_details(
        token=token,
        updated_user_details=updated_user_details
    )

@user_router.put("/profile_picture", status_code=status.HTTP_200_OK)
async def update_profile_picture(profile_picture: UploadFile, token: Token = Depends(deps.get_current_token)):
    
    profile_picture_bytes = await profile_picture.read()

    UserCRUD().update_profile_picture(
        profile_picture_file_bytes=profile_picture_bytes, 
        token=token
    )

    return {"updated": True}

@user_router.delete("/profile_picture", status_code=status.HTTP_200_OK)
def remove_profile_picture(token: Token = Depends(deps.get_current_token)):
    
    UserCRUD().remove_profile_picture(token=token)
    
    return {"removed": True}