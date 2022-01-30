from datetime import datetime
from app.database.db_init import todo_db
from fastapi import HTTPException, status
from app.core.security import PasswordHasher
from app.schemas.auth import UserLogin, UserRegister, UserInDB

user_collection = todo_db['User']
