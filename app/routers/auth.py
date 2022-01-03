from fastapi import APIRouter,Depends,HTTPException,Response,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. database import get_db
from .. import models,schemas,utils,oauth

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def user_login(user_credentails:OAuth2PasswordRequestForm= Depends(),db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==user_credentails.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Invalid email or password!')
    
    if not utils.verify(user_credentails.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Invalid password!')

    access_token = oauth.create_access_token(data={"email":user.email})

    return {"access_token":access_token,"type_token":"bearer"}