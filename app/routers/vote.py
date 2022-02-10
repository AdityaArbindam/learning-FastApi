# this is the API for handling the votes given by a user on a paticular post
from sre_constants import SUCCESS
from ..import model, utils, schemas, jwtauth
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException, APIRouter
from ..db import get_db
from typing import List
from sqlalchemy.orm import session

router = APIRouter(tags=['Votes'])


@router.post("/vote", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: session = Depends(get_db), current_user=Depends(jwtauth.get_current_user)):
    post = db.query(model.Post).filter(model.Post.id == vote.post_id).first()
# this is handling if the user is voting on invalid post
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {vote.post_id} does not exits")

# we are checking if the user voting for post_id x , its present in the vote table or not and whether this user has already voted or not
    vote_query = db.query(model.Votes).filter(
        model.Votes.post_id == vote.post_id, model.Votes.user_id == current_user.id)

    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:   # if you found the vote then it means user has already voted for this post
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} already Voted")

        new_vote = model.Votes(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return{"message": "Sucessfully Added Vote"}
    else:
        if found_vote:
            db.delete(found_vote)
            db.commit()
            return{"message": "Sucessfully deleted Vote"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote Does not exits")
