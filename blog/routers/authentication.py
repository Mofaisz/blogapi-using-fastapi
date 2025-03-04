from fastapi import FastAPI,APIRouter,Depends,status,HTTPException
from .. import schemas,database,models,token
from ..hashing import verify_password
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(
        tags = ["Authentication"]
)

@router.post("/login")
def login(request : OAuth2PasswordRequestForm = Depends(),db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(request.username == models.User.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    if not verify_password(request.password, user.password):  
        raise HTTPException(status_code=401, detail="Invalid password")
    
    access_token = token.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}