import re
from pydantic import ValidationError
from app.core.config import settings
from passlib.context import CryptContext
from fastapi import HTTPException, status

def contains_special_characters(pass1, pass2):
        
    special_character_pattern = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

    if re.search(special_character_pattern, pass2) == None:
        raise ValidationError("Password must contain atleast of any one special characters")
        
    return True

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordHasher:

    @staticmethod
    def hash_password(password):
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(password, hashed_password):
        return pwd_context.verify(password, hashed_password)