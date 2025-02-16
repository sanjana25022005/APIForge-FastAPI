from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
# for optional fields
from typing import Optional
# to create a random integer for id
from random import randrange

# creating an instance of fastapi
app = FastAPI()

# a class that represents what a post should look like
class Post(BaseModel):
    title: str
    content: str
    # optional field for schema
    published: bool = True
    # completely optional field, none will be taken if no value is provided
    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": 
"favorite foods", "content": "I like Biryani", "id": 2}]


@app.get("/")
# async keyword -> the tasks which takes certain amount of time(asynchronous tasks)
# optional : async def root()
def root():
    # fast api converts whatever we are returning into json
    return {"message": "Welcome back"}

# We can add as many methods as we want
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
#def create_posts(payLoad: dict = Body(...)):
    #print(payLoad)
    #return {"message": "successfully created"}
    #return {"new_post": f" title: {payLoad['title']} content: {payLoad['content']}"}

def create_posts(post: Post):
    # post pydantic model converted to an dictionary
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    # brand new post that we have to send back
    return {"data": post_dict}

#def create_posts(post: Post):
#    print(post)
    # for converting pydantic model into dictionary
#    print(post.dict())
#    return {"data": post}

# We need title -> str and content -> str from user


# for retrieving individual post
@app.get("/posts/{id}")
def get_post(id):
    print(id)
    return {"post_detail": f"Here is post {id}"}