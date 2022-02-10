# this will handel database connection

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL='postgres://vdqruomijjvuxs:0b8126f5ccc6f11ce4aff387baeed70c169ca03092ab1928d7df4897c316f922@ec2-18-235-4-83.compute-1.amazonaws.com:5432/ddms4juveivdej'

engine=create_engine(SQLALCHEMY_DATABASE_URL)

sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
