from fastapi import FastAPI, Response, status, HTTPException
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


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

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

@app.post("/posts", status_code=status.HTTP_201_CREATED)
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



# To get the latest post
@app.get("/posts/latest")
def get_latest_Post():
    post = my_posts[len(my_posts) - 1]
    return {"detail": post}

# for retrieving individual post
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} is not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"Post with id: {id} is not found"}
    return {"post_detail": post}


# deleting a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} is not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Update operation
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} is not found")
    # Its gonna take data we recieved from frontend which is stored in postand 
    # its going to convert it into a dictionary
    post_dict = post.dict()
    #To set the ID inside the new dictionary to be that ID
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}