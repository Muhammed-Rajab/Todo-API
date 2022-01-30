from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator
from app.schemas.base import ObjectId, BSONObjectID

class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class UserResponse(BaseModel):
    email: EmailStr
    created: bool = True

class UserInDB(BaseModel):

    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    first_name: str
    last_name: str
    email: EmailStr
    joined: datetime
    hashed_password: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {BSONObjectID: str}

class UserRegister(BaseModel):    
    
    first_name: str = Field(..., max_length=30, )
    last_name: str = Field(..., max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

    @validator('confirm_password')
    def validate_confirm_password(cls,  c_pass, values: dict):
        passwd = values.get('password')
        if passwd == c_pass:
            return c_pass
        raise ValueError("Passwords do not match")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    sub: str
    iat: datetime
    exp: datetime
    type: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"