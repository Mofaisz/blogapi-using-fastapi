from pydantic import BaseModel, EmailStr
from typing import List,Optional



class Blog(BaseModel):
    title:str
    description:str
    body:str


class ShowUser(BaseModel):
    name : str
    email : EmailStr
    class Config():
        orm_mode = True

class ShowBlog(BaseModel):
    id:int
    title:str
    body : str
    owner : Optional[ShowUser]
    
    class Config():
        orm_mode = True

class User(BaseModel):
    name : str
    email : EmailStr
    password : str


class Login(BaseModel):
    username : str
    password : str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None