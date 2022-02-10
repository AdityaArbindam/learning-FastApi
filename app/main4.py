from fastapi import  FastAPI
from app import model
from app.routers.vote import vote
from .db import engine
from .routers import post,user,auth2,vote
model.Base.metadata.create_all(bind=engine)

app = FastAPI()
   
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth2.router)
app.include_router(vote.router)


@app.get("/")
def get_post():
    return {"message":"Hello world"}