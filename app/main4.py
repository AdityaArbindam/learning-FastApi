from fastapi import  FastAPI
from .routers import post,user,auth2,vote



app = FastAPI()
   
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth2.router)
app.include_router(vote.router)


@app.get("/")
def get_post():
    return {"message":"Hello world"}