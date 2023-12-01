from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import engine, get_db, SessionLocal
from app import models, schemas, utils
from .. import oauth2
from typing import List, Optional

router = APIRouter()

# @router.get("/posts", response_model=List[schemas.PostOut])
@router.get("/posts", response_model=List[schemas.PostOut])
async def get_posts(db: Session=Depends(get_db), limit: int=10, skip: int=0, search: Optional[str] = ""):
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # cur.execute(""" Select * FROM posts """)
    # posts = cur.fetchall()
    #print(posts)
    return results

#now we are going to use ****pydantic***
# @app.post("/createposts")
# async def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"new post": f"title {payload['title']} Content: {payload['content']}"}
@router.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: schemas.PostCreate, db: Session=Depends(get_db), current_user: id = Depends(oauth2.get_current_user)):
    # cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #             (post.title, post.content, post.published))
    # new_posts = cur.fetchone()
    # conn.commit()
    # post_dict = post.model_dump()
    # post_dict["id"] = randrange(0,100000)
    # my_posts.append(post_dict)
    # print(post)
    # print(post.model_dump())
    # new_posts = models.Post(title=post.title, content=post.content, published=post.published)
    #insterad make it **
    print(current_user.id)
    new_posts = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return {"data": new_posts}

@router.get("/posts/{id}", response_model=schemas.PostOut)
async def get_posts(id: int, response: Response, db: Session=Depends(get_db), current_user: id = Depends(oauth2.get_current_user)):
    # cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cur.fetchone()
    # post = find_posts(id)
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"data: The requested {id} was not found")
        # response.status_code = 400
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return f"The requested {id} was not found"
    return post

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(id: int, db: Session=Depends(get_db), current_user: id = Depends(oauth2.get_current_user)):
    # cur.execute(""" DELETE from posts where id = %s RETURNING * """, (str(id),))
    # deleted_post = cur.fetchone()
    # conn.commit()
    # index = get_index_posts(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=
                            f"post with {id} doesn't exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=
                            f"owner cant delete different owner id")

    post_query.delete(synchronize_session=False)
    db.commit()
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}")
async def update_posts(id: int, updated_post: schemas.PostCreate, db: Session=Depends(get_db), current_user: id = Depends(oauth2.get_current_user)):
    # cur.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
    #             (post.title, post.content, post.published, str(id),))
    # updated_post = cur.fetchone()
    # conn.commit()
    # index = get_index_posts(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=
                            f"post with {id} doesn't exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=
                            f"owner cant delete different owner id")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    # post_dict = post.model_dump()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    return {"data": post_query.first()}