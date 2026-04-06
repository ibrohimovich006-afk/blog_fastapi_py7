from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas import PostCreate, PostOut, PostUpdate, UserCreate, UserOut
from database import Base, get_db, engine
from models import Post, User

Base.metadata.create_all(bind=engine)

api_router = APIRouter(prefix='/api', tags=['API'])


@api_router.post('/users', response_model=UserOut)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user = User(**user_in.model_dump())

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@api_router.get('/users', response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    stmt = select(User)
    users = db.scalars(stmt).all()
    return users


@api_router.get('/users/{user_id}', response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    stmt = select(User).where(User.id == user_id)
    user = db.scalar(stmt)

    if not user:
        raise HTTPException(status_code=404, detail=f"{user_id}-idli user mavjud emas")

    return user


@api_router.post('/posts', response_model=PostOut)
def create_post(post_in: PostCreate, db: Session = Depends(get_db)):
    stmt = select(User).where(User.id == post_in.user_id)
    user = db.scalar(stmt)

    if not user:
        raise HTTPException(
            status_code=400,
            detail=f"{post_in.user_id}-idli user mavjud emas"
        )

    post = Post(**post_in.model_dump())

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@api_router.get('/posts', response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db)):
    stmt = select(Post)
    posts = db.scalars(stmt).all()
    return posts


@api_router.get('/posts/{post_id}', response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    stmt = select(Post).where(Post.id == post_id)
    post = db.scalar(stmt)

    if not post:
        raise HTTPException(status_code=404, detail=f"{post_id}-idli post mavjud emas")

    return post


@api_router.put('/posts/{post_id}', response_model=PostOut)
def update_post(post_id: int, post_in: PostUpdate, db: Session = Depends(get_db)):
    stmt = select(Post).where(Post.id == post_id)
    post = db.scalar(stmt)

    if not post:
        raise HTTPException(status_code=404, detail=f"{post_id}-idli post mavjud emas")

    stmt = select(User).where(User.id == post_in.user_id)
    user = db.scalar(stmt)

    if not user:
        raise HTTPException(
            status_code=400,
            detail=f"{post_in.user_id}-idli user mavjud emas"
        )

    post.title = post_in.title
    post.content = post_in.content
    post.user_id = post_in.user_id

    db.commit()
    db.refresh(post)

    return post


@api_router.delete('/posts/{post_id}')
def delete_post(post_id: int, db: Session = Depends(get_db)):
    stmt = select(Post).where(Post.id == post_id)
    post = db.scalar(stmt)

    if not post:
        raise HTTPException(status_code=404, detail=f"{post_id}-idli post mavjud emas")

    db.delete(post)
    db.commit()

    return {"message": "Post deleted successfully"}