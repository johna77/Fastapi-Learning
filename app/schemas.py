from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass   

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

#this class will add in @app route in main.py to show what data we would like to shouw at frontend siocne our
#data is not dict so we will use https://fastapi.tiangolo.com/tutorial/sql-databases/?h=sql
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id : int
    owner: UserOut
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True 

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Auth(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str

class Vote(BaseModel):
    post_id: int
    dir: int