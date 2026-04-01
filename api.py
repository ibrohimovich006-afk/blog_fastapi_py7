from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Post
from schemas import PostCreate, PostOut, PostUpdate

Base.metadata.create_all(bind=engine)

api_router = APIRouter(prefix='/api/posts', tags=['Posts'])


@api_router.post('/', response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(post_in: PostCreate, db: Session = Depends(get_db)):
    post = Post(**post_in.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@api_router.get('/', response_model=List[PostOut])
def list_posts(db: Session = Depends(get_db)):
    stmt = select(Post).order_by(Post.id.desc())
    return db.scalars(stmt).all()


@api_router.get('/{post_id}/', response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    stmt = select(Post).where(Post.id == post_id)
    post = db.scalar(stmt)
    if post is None:
        raise HTTPException(status_code=404, detail='Post topilmadi')
    return post


@api_router.put('/{post_id}/', response_model=PostOut)
def update_post(post_id: int, post_in: PostUpdate, db: Session = Depends(get_db)):
    stmt = select(Post).where(Post.id == post_id)
    post = db.scalar(stmt)
    if post is None:
        raise HTTPException(status_code=404, detail='Post topilmadi')

    for key, value in post_in.model_dump().items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)
    return post


@api_router.delete('/{post_id}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    stmt = select(Post).where(Post.id == post_id)
    post = db.scalar(stmt)
    if post is None:
        raise HTTPException(status_code=404, detail='Post topilmadi')

    db.delete(post)
    db.commit()
    return None
