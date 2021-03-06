

from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)

# @router.get("/posts", response_model=List[schemas.Post]) # without prefix
#@router.get("/", response_model=List[schemas.Post])
@router.get("/")
#@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user), 
limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #posts = db.query(models.Post).all()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(results)
    return results

    # posts = db.query(models.Post).filter(models.Post.owner_id == int(current_user.id)).all() #get all own posts
    #return posts



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
 
    # new_post = models.Post(title=post.title, content=post.content, published = post.published)
    new_post = models.Post(owner_id=current_user.id, **post.dict()) # to replace the above line

    #print(current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post


# get latest 3 posts
@router.get("/latest", response_model=List[schemas.Post])
def get_post_latest(db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    number = db.query(models.Post).count()
    post = db.query(models.Post).offset(number-3).all()
    return  post


#@router.get("/{id}", response_model=schemas.PostOut)
@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    # print(post)
    return  post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")

    if post.owner_id != int(current_user.id):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    print(post.owner_id)
    print(current_user.id)
    if post.owner_id != int(current_user.id):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
