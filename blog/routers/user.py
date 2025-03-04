from fastapi import APIRouter,Depends,status,HTTPException
from passlib.context import CryptContext
from .. import schemas,database,models
from sqlalchemy.orm import Session
from ..repository import user
from ..hashing import hash_password



router = APIRouter(
    prefix = "/user",
    tags = ["User"]
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#for user -creating a user
@router.post("/",response_model = schemas.ShowUser)
def user(request : schemas.User, db: Session = Depends(database.get_db)):
    hashed_password = hash_password(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model = schemas.ShowUser)
def showUser(id:int,db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with given id is not found")
    return user

@router.delete("/id", status_code = status.HTTP_201_CREATED)
def destroy_user(id:int,db: Session = Depends(database.get_db)):
    db.query(models.User).filter(id ==models.User.id).delete(synchronize_session=False)
    db.commit()
    return f"User {id} deleted"
    # return destroy_user_repo(id,db)