from operator import index
from sqlite3 import Cursor, DatabaseError
from turtle import title
from typing import Optional
from urllib import response
from xmlrpc.client import boolean
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2   # this is the library used to make connectin with the database
from psycopg2.extras import RealDictCursor
app = FastAPI()


class post(BaseModel):
    title: str
    content: str
    published: boolean = True
    rating: Optional[int] = None


try:
    conn = psycopg2.connect(host="localhost",database='FastApi',user='postgres',password='aditya123',cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("database connection was successful")

except Exception as error:
    print("Not able to connect")
    print("Error:", error)


@app.get("/posts")
def get_post():
    cursor.execute(""" select * from post """)
    post=cursor.fetchall()
    return post


@app.get("/posts/{id}")
def get_post(id:int ):
    cursor.execute(""" select * from post where id=%s RETURNING *""",(str(id)))
    post=cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No Post with id: {id} found ")
    return {"Data": post}


@app.post("/posts")
def create_post(post: post, status_code=status.HTTP_201_CREATED):
    cursor.execute(""" insert into post(title,content,published) values(%s,%s,%s) RETURNING *""",
                   (post.title,post.content,post.published))
    post=cursor.fetchone()  # to fetch one post
    print(post)
    conn.commit()
    return {"data": post}


@app.delete("/posts/{id}")
def delete_post(id: int):

    cursor.execute(""" delete from post where id=%s returning *""",(str(id)))
    post=cursor.fetchone()
    if post==None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="no post dound")
    conn.commit()
    return {"Message": "Post deleted Sucessfully"}


@app.put("/posts/{id}")
def update_post(id: int, post: post):

    cursor.execute(""" update post set title=%s,content=%s,published=%s where id=%s returning *""",(post.title,post.content,post.published,(str(id))))
    updated_post=cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no post Found")
    return updated_post
