from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import session
from app import utils
from .db import get_db
import schemas,model,jwtauth
from .utils import hash
router=APIRouter(tags=['Authenticate'])

@router.post("/login")
def login(user_credentials: schemas.UserLogin,db: session = Depends(get_db)):

    # for valid login we are first checking if the email matches

    user=db.query(model.User).filter(model.User.email==user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not found")
    
    # now we are checking for valid email

    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found")
    
    # as both the fields are validated now we will create and pass token
    access_token=jwtauth.create_access_token(data={"user_id":user.id})  # sending like this because it will take input as dictionary
    return {"access_token": access_token,"token_type":"bearer"} 
    
    
