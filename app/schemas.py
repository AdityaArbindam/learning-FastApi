from importlib.resources import contents
from typing import Optional
from pydantic import BaseModel, EmailStr,conint
from sqlalchemy import true
from datetime import datetime


# creating diffrent models for diffrent request

class Userout(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class Postcreate(PostBase):
    pass

# making pydantic model to handel response


class Post(PostBase):  # its inherating the class of PostBase
    id: int
    created_at: datetime
    user_id: int
    owner: Userout
# we are crating post in a sqlalchemy model but generating response through pydantic model so here we saying to config the ORM mode with pydantic mdoel

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

# response for create user


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)   # less then eual to 1
