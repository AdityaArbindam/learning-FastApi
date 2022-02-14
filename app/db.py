# this will handel database connection
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL='postgresql://cftkqehxzdnsus:c465a8f67391eec828ad893158ea1e260b308ce0fe76e1389d5f509f29dbbd75@ec2-18-215-8-186.compute-1.amazonaws.com:5432/dfh4r890b65f6r'

engine=create_engine(DATABASE_URL)

sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
