# creating Token

from base64 import encode
from fastapi import Depends, status, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
from .import schemas
from fastapi.security import OAuth2PasswordBearer

# secutity key
# algorithm you are using
# exprition Time

# this will take you to auth2.py into the login router
oath2_schema = OAuth2PasswordBearer(tokenUrl='/login')

SECRET_KEY = "FALNFLJFNSLDMFSDMFSMFSMFDSKFMFM"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):   # here data is the payload
    to_encode = data.copy()

    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id: str = payload.get("user_id")
        if not id:
            raise credential_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credential_exception
    return token_data


def get_current_user(token: str = Depends(oath2_schema)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not verify credentials",
                                         headers={"www-Authenticate": "Bearer"})
    return verify_access_token(token, credential_exception)
