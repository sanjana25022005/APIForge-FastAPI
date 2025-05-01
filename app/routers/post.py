from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": 
"favorite foods", "content": "I like Biryani", "id": 2}]

# To test the sqlalchemy connection
#@app.get("/sqlalchemy")
#def test_posts(db: Session = Depends(get_db)):
#    posts = db.query(models.Post).all()
#    return {"data": posts}


# We can add as many methods as we want
@router.get("/", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()

    #using SQLAlchemy
    posts = db.query(models.Post).all()
    return posts


#def create_posts(payLoad: dict = Body(...)):
    #print(payLoad)
    #return {"message": "successfully created"}
    #return {"new_post": f" title: {payLoad['title']} content: {payLoad['content']}"}

#def create_posts(post: Post):
    # post pydantic model converted to an dictionary
    #post_dict = post.dict()
    #post_dict['id'] = randrange(0, 1000000)
    #my_posts.append(post_dict)
    # brand new post that we have to send back
    #return {"data": post_dict}
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = 
                 Depends(oauth2.get_current_user)):
    # post pydantic model converted to an dictionary
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #               (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()

    #sqlalchemy
    print(current_user.email)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post




#def create_posts(post: Post):
#    print(post)
    # for converting pydantic model into dictionary
#    print(post.dict())
#    return {"data": post}

# We need title -> str and content -> str from user


# To get the latest post
@router.get("/latest")
def get_latest_Post():
    post = my_posts[len(my_posts) - 1]
    return {"detail": post}

# for retrieving individual post
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" SELECT * FROM posts WHERE id = %s""", str((id),))
    #post = cursor.fetchone()
    #conn.commit()

    #sqlalchemy
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} is not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"Post with id: {id} is not found"}
    return post


# deleting a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = 
                 Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()

    #sqlalchemy
    post = post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} is not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#Update operation
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = 
                 Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #               (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()

    #sqlalchemy
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} is not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()