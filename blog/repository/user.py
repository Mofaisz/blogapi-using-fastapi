from .. import schemas,models
from sqlalchemy.orm import Session
from fastapi import FastAPI,HTTPException,status


def create_user(request:schemas.User,db:Session):
    hashed_password = hash_password(request.password)
    new_user = User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def destroy_user_repo(id:int,db: Session):
    db.query(models.User).filter(id ==models.User.id).delete(synchronize_session=False)
    db.commit()
    return f"User {id} deleted"