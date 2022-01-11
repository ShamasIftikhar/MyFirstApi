from hashlib import new
from json import detect_encoding
from os import stat
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from pydantic.types import PositiveFloat
from sqlalchemy.orm.session import Session
from starlette.responses import Response
from .. import schemas, oauth, models
from ..database import get_db


router = APIRouter(prefix='/votes', tags=['Voting'])


@router.post("/")
def vote(vote: schemas.vote, db: Session = Depends(get_db), current_user: int = Depends(oauth.Get_current_User)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {vote.post_id} doesn't exist")
    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id, models.Votes.user_email == current_user.email)
    found_vote = vote_query.first()
    if not found_vote:
        new_vote = models.Votes(post_id=vote.post_id,
                                user_email=current_user.email)
        db.add(new_vote)
        db.commit()
        raise HTTPException(status_code=status.HTTP_201_CREATED,
                            detail="successfully created vote")
    else:
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
