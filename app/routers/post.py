from ..import model, utils, schemas, jwtauth
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException, APIRouter
from ..db import get_db
from typing import List
from sqlalchemy.orm import session

router = APIRouter(tags=['Posts'])


@router.get("/posts", response_model=List[schemas.Post])
def get_post(db: session = Depends(get_db), current_user=Depends(jwtauth.get_current_user)):
    posts = db.query(model.Post).all()
    return posts


@router.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: session = Depends(get_db), current_user=Depends(jwtauth.get_current_user)):

    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Post with id: {id} found ")
    return post


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.Postcreate, db: session = Depends(get_db), current_user: int = Depends(jwtauth.get_current_user)):
    # This "user_id:int=Depends(jwtauth.get_current_user)" dependency will make sure user is loged in
    new_post = model.Post(
        title=post.title, content=post.content, published=post.published, user_id=current_user.id)

    # you can also use new_post=mod el.Post(**post.dict())  it means you are converting the post in dictionary and then unpacking it to get all the columns.
    # it will be helpful if user is giving losts of imputs or columns

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/posts/{id}")
def delete_post(id: int, db: session = Depends(get_db), current_user: int = Depends(jwtauth.get_current_user)):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no post dound with id:{id}")
    db.delete(post)
    db.commit()
    return {"post_deleted": post}


# to update posts
@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.Postcreate, db: session = Depends(get_db), current_user: int = Depends(jwtauth.get_current_user)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    updated_post = post_query.first()
    print(updated_post)
    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no post Found with id: {id}")
    post_query.update(post.dict())
    db.commit()
    return post_query.first()
