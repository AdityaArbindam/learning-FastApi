from multiprocessing import synchronize
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException
from sqlalchemy.orm import session
from .import model, schemas
from .db import engine, get_db
from typing import  List
from .utils import hash
from app import utils

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

# geting all the posts


# we have to pust list in the response beacuse we are retreving multiple post as a list from the database and if we pass response on the basis of post it will give error
@app.get("/posts", response_model=List[schemas.Post])
def get_post(db: session = Depends(get_db)):
    posts = db.query(model.Post).all()
    print(posts)
    return posts


# getting post with a paticular id
@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: session = Depends(get_db)):

    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Post with id: {id} found ")
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.Postcreate, db: session = Depends(get_db)):

    new_post = model.Post(
        title=post.title, content=post.content, published=post.published)

    # you can also use new_post=mod el.Post(**post.dict())  it means you are converting the post in dictionary and then unpacking it to get all the columns.
    # it will be helpful if user is giving losts of imputs or columns

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# handel delete


@app.delete("/posts/{id}")
def delete_post(id: int, db: session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no post dound with id:{id}")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# to update posts
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.Postcreate, db: session = Depends(get_db)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    updated_post = post_query.first()
    print(updated_post)
    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no post Found with id: {id}")
    post_query.update(post.dict())
    db.commit()
    return post_query.first()

# API to Create new Users


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.Userout)
def create_user(user: schemas.UserCreate, db: session = Depends(get_db)):
    # hash the password -user.password
    # calling the hash function inside utils.py File
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # taking email and password from the user and matching with the database User model
    new_user = model.User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{id}",response_model=schemas.Userout)
def get_user(id: int, db: session = Depends(get_db)):
   user = db.query(model.User).filter(model.User.id == id).first()

   if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details=f" User with id: {id} not  found")
   return user