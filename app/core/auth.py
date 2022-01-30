import jwt
from typing import Optional, Union
from app.core.config import settings
from app.database.db_init import todo_db
from datetime import datetime, timedelta
from app.schemas.auth import UserInDB, Token
from app.core.security import PasswordHasher
from fastapi.security import OAuth2PasswordBearer

user_collection = todo_db['User']

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/auth/login")

def authenticate(email: str, password: str) ->  Optional[Union[bool, UserInDB]]:
    
    user = user_collection.find_one({'email': email})
    
    if not user: return False
    if not PasswordHasher.verify_password(password, user.get('hashed_password')):return False

    return UserInDB(**user)

class TokenHandler:

    @staticmethod
    def signJWT(sub: str, token_type: str = "access_token") -> str:
        
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION_TIME)
        token = Token(sub=sub, iat=datetime.now(), exp=expire, type=token_type)

        return jwt.encode(payload=token.dict(), key=settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def decodeJWT(token: str) -> Optional[Union[dict, Token]]:

        try:
            decoded_token = jwt.decode(
                jwt=token, 
                key=settings.JWT_SECRET, 
                algorithms=[settings.JWT_ALGORITHM], 
                options={"verify_aud": False}
            )
            return Token(**decoded_token)
        
        except:
            return {}