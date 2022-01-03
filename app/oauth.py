from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import JWTError,jwt
from datetime import datetime,timedelta
from pydantic.networks import EmailStr
from sqlalchemy.orm.session import Session
from starlette import status
from app import models
from . import schemas,database
from .config import setting

oauth2_scheme = OAuth2PasswordBearer('login')

SECRET_KEY = setting.secret_key
ALGORITHM=setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=setting.access_token_expiration_minutes

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credentials_expection):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email:str =payload.get("email")

        if email is None:
            raise credentials_expection
        token_data=schemas.TokenData(email=email)
    except JWTError:
        raise credentials_expection

    return token_data

def Get_current_User(token:str= Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
    credentials_expection = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'Coulad not validate credentials',headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token,credentials_expection)
    user = db.query(models.User).filter(models.User.email==token.email).first() 

    return user
