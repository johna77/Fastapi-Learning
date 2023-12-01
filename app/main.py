from fastapi import FastAPI
from app import models
from app.database import engine
from .router import user, post, auth, vote

models.Base.metadata.create_all(bind=engine)

app= FastAPI()

# my_posts = [{"title": "this is 1st title", "content": "This is the content of 1st title", "id": 1},
#             {"title": "this is 2nd title", "content": "This is the content of 2nd title", "id": 2}]

# def find_posts(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

# def get_index_posts(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i 

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Hello its me!!!"}
