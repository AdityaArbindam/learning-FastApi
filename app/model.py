# importing the db.py file we created to connect the database and API using SqlAlchemy
from tkinter import CASCADE
from tkinter.tix import Tree
from .db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy .sql.expression import text
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete=CASCADE), nullable=False)
    owner = relationship("User")
    

class User(Base):
    __tablename__ = "users"

    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

class Votes(Base):
    __tablename__="votes"
    user_id=Column(Integer,ForeignKey("users.id",ondelete=CASCADE),primary_key=True,nullable=False)
    post_id=Column(Integer,ForeignKey("posts.id",ondelete=CASCADE),primary_key=True,nullable=False)