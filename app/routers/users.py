from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm.session import Session
from .. import schemas, models, utils
from ..database import get_db

router = APIRouter(prefix="/users", tags=['Users'])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.Users, db: Session = Depends(get_db)):
    res = db.query(models.Post).filter(models.User.email==user.email).first()
    if not res:
        user.password = utils.hash(user.password)
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    elif res:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Email\"{user.email}\" already exist!')


@router.get("/{id}", response_model=schemas.GetUserResponse)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The User with id : '{id}' was not found")

    return user
