from fastapi import Body, FastAPI, APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, utils

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):

    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session=Depends(get_db)):
    post = db.query(models.User).filter(models.User.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=
                            f"post with {id} doesn't exist")
    return post
