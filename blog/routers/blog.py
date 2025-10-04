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
def create(blog:schemas.Blog,db:Session = Depends(database.get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    # return {"details":f"{blog.title} is interesting","data":blog}
    new_blog = models.Blog(title = blog.title,description = blog.description , body = blog.body,user_id = current_user.id)
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

@router.post("/blogs/{id}/like")
async def post_likes(id:int,
db:Session = Depends(database.get_db)
,get_current_user:schemas.User = Depends(oauth2.get_current_user)):
    # first check if blog exist or not
    blog = db.query(models.Blog).filter(models.Blog.id ==id).first()
    if not blog:
        raise HTTPException(status_code=404,detail="blog not found")
    

    # now check wether the blog is already liked or not
    existing_like = db.query(models.Like).filter(models.Like.blog_id ==id,models.Like.user_id==get_current_user.id).first()
    if existing_like:
        # raise HTTPException(status_code=409,detail = "Already liked")
        db.delete(existing_like)
        db.commit()
        # db.refresh()
        return {"message": "Like removed (unliked)"}

    new_like = models.Like(blog_id=id,user_id=get_current_user.id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return {"message" :"BLog liked successfully","like-id":new_like.id}



# Get likes count
@router.get("/{id}/likes")
def get_likes(id:int,db:Session=Depends(database.get_db),get_current_user:schemas.User = Depends(oauth2.get_current_user)):
    total_likes = db.query(models.Like).filter(models.Like.blog_id==id).count()
    user_liked = db.query(models.Like).filter(models.Like.blog_id == id,models.Like.user_id==get_current_user.id).first() is not None
    return {"likes":total_likes,"Liked-by":user_liked}


@router.post("/{id}/comment")
def add_comment(id:int,content:str ,db:Session = Depends(database.get_db),get_current_user:schemas.User = Depends(oauth2.get_current_user)):
    # first check if comments exist or not
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail = "blog not found")


    #then checks if user has already commented or not 
    # existing_comment = db.query(models.Comments).filter(models.Comments.blog_id==id,models.Comments.user_id==get_current_user.id).first()
    # if existing_comment

    #then add new comment 
    new_comment = models.Comments(content=content,user_id = get_current_user.id, blog_id = id)
    db.add(new_comment)
    db.commit()
    return {"message" : "comment added successfully"}


@router.get("/{id}/comments")
def get_comments(id:int,db:Session = Depends(database.get_db),get_current_user:schemas.User = Depends(oauth2.get_current_user)):

    get_comment = db.query(models.Comments).filter(models.Comments.blog_id==id).all()
    total_comment = db.query(models.Comments).filter(models.Comments.blog_id==id).count()
    return {"comments":get_comment, "total_comment":total_comment}