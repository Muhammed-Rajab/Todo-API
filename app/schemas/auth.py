from datetime import datetime
from fastapi import Form, HTTPException, status
from pydantic import BaseModel, EmailStr, Field, validator
from app.schemas.base import ObjectId, BSONObjectID

class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    joined: datetime
    profile_picture_name: str

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
    profile_picture_name: str

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
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Passwords do not match")

class UserRegisterForm(UserRegister):
    # Inherits from User Register class
    # This class basically accepts register data
    # In the form of Form Class, so that we can parse and validate them using pydantic
    def __init__(
        self,
        first_name: str = Form(..., max_length=30),
        last_name: str = Form(..., max_length=30),
        email: str = Form(..., max_length=255),
        password: str = Form(..., min_length=8),
        confirm_password: str = Form(..., min_length=8)
        ):
        
        super().__init__(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            confirm_password=confirm_password
        )

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    first_name: str = Field(..., max_length=30)
    last_name: str = Field(..., max_length=30)

class  UserUpdateForm(UserUpdate):

    def __init__(
        self,
        first_name: str = Form(..., max_length=30),
        last_name: str = Form(..., max_length=30),
        ):
        
        super().__init__(
            first_name=first_name,
            last_name=last_name
        )

class Token(BaseModel):
    sub: str
    iat: datetime
    exp: datetime
    type: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"