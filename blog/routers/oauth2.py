from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .. import token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #tokenUrl says where you want to fetch data rn -->login

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Invalid authentication")
    
    return token.verify_access_token(data,credentials_exception)
