from app.schemas.base import ObjectId
from app.schemas.auth import User, Token
from app.database.db_init import user_collection
from fastapi import Depends, HTTPException, status
from app.core.auth import oauth2_scheme, TokenHandler

def get_current_user(token: str =  Depends(oauth2_scheme)) -> User:
    
    decoded_token = TokenHandler().decodeJWT(token)
    
    if decoded_token:
        _id = decoded_token.sub
        user = user_collection.find_one({'_id': ObjectId(_id)})
        if user:
            return User(**user)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

def get_current_token(token: str = Depends(oauth2_scheme)) -> Token:
    return TokenHandler().decodeJWT(token)