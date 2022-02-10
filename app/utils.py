# this files contains the logic for hashing a password
from passlib.context import CryptContext

pwd_context =CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password:str):
    return pwd_context.hash(password)



# this function will automatically verify that whether password matches or not
def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)
