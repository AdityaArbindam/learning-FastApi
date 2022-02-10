from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import session
from app import utils
from ..db import get_db
from .. import schemas,model,jwtauth
from ..utils import hash
from fastapi.security.oauth2 import OAuth2PasswordRequestForm



router=APIRouter(tags=['Authenticate'])

@router.post("/login",response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(),db: session = Depends(get_db)):

    # for valid login we are first checking if the email matches

    user=db.query(model.User).filter(model.User.email==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"not found")
    
    # now we are checking for valid email

    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not found")
    
    # as both the fields are validated now we will create and pass token
    access_token=jwtauth.create_access_token(data={"user_id":user.id})  # sending like this because it will take input as dictionary
    
    return {"access_token": access_token,"token_type":"bearer"}
    
    
# here we are using the "OAuth2PasswordRequestForm" to get the user inputs , it will take the user input in the form of form data