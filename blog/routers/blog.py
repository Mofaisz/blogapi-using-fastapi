from fastapi import APIRouter,Depends,status,HTTPException
from .. import schemas,database,models
from typing import List
from sqlalchemy.orm import Session
from ..repository import blog
from ..routers import oauth2
# router = APIRouter(prefix="/blog", tags=["Blogs"])
router = APIRouter(
    prefix = "/blog",
    tags = ["Blogs"]
)

@router.post("/")
def create(blog:schemas.Blog,db:Session = Depends(database.get_db),get_current_user:schemas.User = Depends(oauth2.get_current_user)):
    # return {"details":f"{blog.title} is interesting","data":blog}
    new_blog = models.Blog(title = blog.title,description = blog.description , body = blog.body,user_id = get_current_user.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"message":"blog created successfully","blog:":new_blog}

    # return blog.create(request, db)



@router.get("/",response_model = List[schemas.ShowBlog])
def get_all_blog(db:Session = Depends(database.get_db),get_current_user:schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)


@router.get("/{id}",response_model = schemas.ShowBlog)
def get_blog_by_id(id:int, db: Session = Depends(database.get_db),get_current_user:schemas.User = Depends(oauth2.get_current_user)):
     return blog.get_blog_by_id(id,db)



@router.delete("/{id}", status_code = status.HTTP_201_CREATED)
def delete(id:int,db: Session = Depends(database.get_db),get_current_user:schemas.User = Depends(oauth2.get_current_user)):
    return blog.destroy(id,db)


#to update existing blog
@router.put("/{id}",status_code = 202)
def update_blog(id,blog:schemas.Blog, db: Session = Depends(database.get_db),get_current_user:schemas.User = Depends(oauth2.get_current_user)):
    blog_db = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog_db.first():
        raise HTTPException(status_code=404, detail="Item not found")
    
    blog_db.update(blog.dict())
    db.commit()
    return "blog updated"
