from app.core.config import settings
from passlib.context import CryptContext
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordHasher:

    @staticmethod
    def hash_password(password):
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(password, hashed_password):
        return pwd_context.verify(password, hashed_password)