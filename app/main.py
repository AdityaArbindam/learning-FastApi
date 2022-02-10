from operator import index
from turtle import title
from typing import Optional
from xmlrpc.client import boolean
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
# we improt the randomrange  so that we can use it to generate id for our posts
from random import randrange
app = FastAPI()                    # creating the instance of Fastapi


class post(BaseModel):    # this class will validate if the frontend have provided proper fromat or not
    title: str
    content: str
    # this optional for the user to provide its default value is true
    published: boolean = True
    # optional [int] specifies that user may give it or may not and we set default as None
    rating: Optional[int] = None


# we are creating my_post an array of dictionary and hardcode somevalues but we can append ne post into it
my_post = [{"title": " Aditya Arbidam", "content": "started Working in Infy",
            "id": 1}, {"titile": "favouirate food", "content": "Pizza", "id": 2}]


def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p

# creating end point to get post from database also called path/decorater for a given ID


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
        # OR
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message": f"post with '{id}' was not found"}
    # return statement is used to display data we want user shall see
    return {"post_deatails": post}


# path to read multiple post
@app.get('/posts')
def get_post():
    return {'data': my_post}


# Path to create a post
@app.post('/posts')
# we already defined a post class using pydantic basemodel now we are storing it as post here
def create_post(post: post, status_code=status.HTTP_201_CREATED):
    post_new = post.dict()
    # here we are using the randrange and we can assign any no from 0 to 10000
    post_new['id'] = randrange(0, 10000)
    # appending the post into our array of dictionary
    my_post.append(post_new)
    return {"data": post_new}
# def create_post(payload : dict=Body(...)): # this will import body from the fast api and give it to payload for this we have imported body from FastApi
#   print(payload)
#    return {"new_post":f"titile:{payload['title']} content: {payload['content']}"}


# making and end point to delete the post


def find_post_index(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i


@app.delete("/posts/{id}")
def delete_post(id: int, status_code=status.HTTP_204_NO_CONTENT):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with '{id}' not found")
    my_post.pop(index)
    return {"message": "Post Deleted Sucessfully"}


@app.put("/posts/{id}")
def update_posts(post: post, id: int):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with '{id}' not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_post[index] = post_dict
    return {"Data": post_dict}
