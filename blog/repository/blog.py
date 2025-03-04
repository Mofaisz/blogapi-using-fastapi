from .. import models,schemas
from sqlalchemy.orm import Session
from fastapi import FastAPI,HTTPException,status,Depends




def get_all(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create_blog(blog:schemas.Blog,db:Session):
    new_blog = models.Blog(title = blog.title,description = blog.description , body = blog.body,user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"message":"blog created successfully","blog:":new_blog}

def get_blog_by_id(id,db):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


def destroy(id,db):
    db.query(models.Blog).filter(id == models.Blog.id).delete(synchronize_session=False)
    db.commit()
    return "blog deleted"

def update(id,blog,db):
    blog_db = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog_db.first():
        raise HTTPException(status_code=404, detail="Item not found")
    
    blog_db.update(blog.dict())
    db.commit()
    return "blog updated"