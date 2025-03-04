from fastapi import FastAPI,Depends
from pydantic import BaseModel
from .database import engine, Base,SessionLocal,get_db
from . import models,schemas
from sqlalchemy.orm import Session,relationship
from typing import List
from passlib.context import CryptContext
from .routers import blog,user,authentication


app = FastAPI(
)


Base.metadata.create_all(bind=engine)


app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)
