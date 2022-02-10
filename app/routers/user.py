from ..import model,utils,schemas,jwtauth
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException,APIRouter
from ..db import get_db
from sqlalchemy.orm import session
from typing import  List
from app import jwtauth

router=APIRouter(tags=['Users'])

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.Userout)
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


@router.get("/users/{id}",response_model=schemas.Userout)
def get_user(id: int, db: session = Depends(get_db),current_user: int = Depends(jwtauth.get_current_user)):
   user = db.query(model.User).filter(model.User.id == id).first()

   if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details=f" User with id: {id} not  found")
   return user

@router.get("/users",response_model=List[schemas.Userout])
def get_users(db: session = Depends(get_db), user_id: int = Depends(jwtauth.get_current_user)):
    users=db.query(model.User).all()
    return users

