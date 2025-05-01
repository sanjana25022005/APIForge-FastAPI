from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
# for optional fields
from typing import Optional, List
# to create a random integer for id
from random import randrange
# for connecting to the database
import psycopg2
from psycopg2.extras import RealDictCursor 
# After error, we want to make it wait before it tries to reconnect
from sqlalchemy.orm import Session
import time
from . import models, schemas, utils
from .schemas import Post
from .database import engine, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

# creating an instance of fastapi
app = FastAPI()



# continuously runs until we successfully get a connection
while True:
    # to connect to the database
    try:
        # we have to pass in few properties 
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
                                password='25Feb@005', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    # storing the error in a variable called error
    except Exception as error:
        print("Failed to connect to the database")
        # printing the error
        print("error was: ", error)
        # wait for 2 seconds before trying to connect again
        time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": 
"favorite foods", "content": "I like Biryani", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
# async keyword -> the tasks which takes certain amount of time(asynchronous tasks)
# optional : async def root()
def root():
    # fast api converts whatever we are returning into json
    return {"message": "Welcome back"}

