from sys import prefix
from typing import List, Optional
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.orm.session import Session
from fastapi.staticfiles import StaticFiles
from sqlalchemy.sql.functions import count
from starlette.requests import Request
from .. import schemas, models, oauth
from ..database import get_db
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/posts", tags=['Posts'])

router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@router.get("/", response_model= List[schemas.PostOut])
def Get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post, count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def createposts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth.Get_current_User)):
    print(current_user.email)
    new_post = models.Post(**post.dict(), owner_email=current_user.email,)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def Get_sposts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post, count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The Post with id : '{id}' was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.Get_current_User)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    print(current_user)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The Post with id : '{id}' was not found")

    if post.owner_email != current_user.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You can't perfortm the specified action!")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_posts(id: int, poster: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth.Get_current_User)):
    print(current_user)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The Post with id : '{id}' was not found")
    if post.owner_email != current_user.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You can't perfortm the specified action!")
    post_query.update(poster.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
