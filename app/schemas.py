from datetime import datetime
from pydantic import BaseModel
from pydantic.networks import EmailStr
from sqlalchemy.sql.sqltypes import String


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class Config:
    orm_mode = True


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime
    owner: UserResponse

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int
    
    class Config:
        orm_mode = True


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        orm_mode = True


class Users(BaseModel):
    email: EmailStr
    password: str


class GetUserResponse(UserResponse):
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


class vote(BaseModel):
    post_id: int
