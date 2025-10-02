from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from .. import token,database,models
from sqlalchemy.orm import Session



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #tokenUrl says where you want to fetch data rn -->login

# def get_current_user(data: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(status_code=401, detail="Invalid authentication")
    
#     return token.verify_access_token(data,credentials_exception)
def get_current_user(
    data: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication"
    )
    
    payload = token.verify_access_token(data, credentials_exception)
    email: str = payload.get("sub")  
    
    if email is None:
        raise credentials_exception

    # Fetch from DB
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    print(user.id)
    return user 

