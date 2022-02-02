import string
import random
from typing import Any, Dict
from datetime import datetime
from app.core.config import settings
from app.schemas.base import ObjectId
from fastapi import HTTPException, status
from app.core.security import PasswordHasher
from app.database.db_init import user_collection, todos_collection
from app.schemas.auth import Token, UserLogin, UserRegister, UserInDB, UserResponse

class UserCRUD:

    def _save_profile_picture(self, profile_picture: bytes) -> Dict[str, Any]:
        
        if not profile_picture: return "default.png"

        random_file_name = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 12))
        with open(
            f"{settings.BASE_PATH}/{settings.PROFILEPICTURES_DIR}/{random_file_name}.png", "wb") as file:
            file.write(profile_picture)
        return random_file_name+".png"

    def _create_user(self, 
            register_data: UserRegister, 
            profile_picture: bytes) -> UserInDB:
        hashed_password: str = PasswordHasher().hash_password(register_data.password)
        joined: datetime = datetime.now()

        profile_picture_name = self._save_profile_picture(profile_picture)
        return UserInDB(
            **register_data.dict(), 
            hashed_password=hashed_password, 
            joined=joined, 
            profile_picture_name=profile_picture_name)


    def create(self, register_data: UserRegister, profile_picture: bytes) -> UserResponse:
    
        # If user already exists, raise HTTPException
        # else create a new user
        user_already_exists = user_collection.find_one({'email': register_data.email})

        if user_already_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email {register_data.email} already exists.")
        
        new_user: UserInDB = self._create_user(register_data, profile_picture=profile_picture)
        user_collection.insert_one(new_user.dict(by_alias=True))
        return UserResponse(**new_user.dict())
    
    def delete(self, token: Token):
        
        deleted_user = user_collection.find_one_and_delete({'_id': ObjectId(token.sub)})

        if deleted_user:
            todos_collection.delete_many({
                'user__id': ObjectId(token.sub)
            })
            return True
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exists.")