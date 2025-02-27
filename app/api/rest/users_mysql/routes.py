from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.mysql.database import get_db
from app.mysql.models import Post, User

from .schemas import *

db = Annotated[AsyncSession, Depends(get_db)]


router = APIRouter(prefix="/mysql", tags=["users-mysql"])


@router.post("/users/", response_model=UserInDB)
async def create_user(user: UserCreate, db: db):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}", response_model=UserInDB)
async def get_user(user_id: int, db: db):
    result = await db.execute(select(User).options(selectinload(User.posts)).filter(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.get("/users/", response_model=list[UserInDB])
async def get_users(db: db, skip: int = 0, limit: int = 100):
    result = await db.execute(select(User).options(selectinload(User.posts)).offset(skip).limit(limit))
    return result.scalars().all()

@router.put("/users/{user_id}", response_model=UserInDB)
async def update_user_put(user_id: int, user: UserPut, db: db):
    db_user = await db.execute(select(User).filter(User.id == user_id))
    db_user = db_user.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db_user.username = user.username
    db_user.email = user.email

    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.patch("/users/{user_id}", response_model=UserInDB)
async def update_user_patch(user_id: int, user: UserPatch, db: db):
    db_user = await db.execute(select(User).filter(User.id == user_id))
    db_user = db_user.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.username:
        db_user.username = user.username
    if user.email:
        db_user.email = user.email

    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}", response_model=UserInDB)
async def delete_user(user_id: int, db: db):
    db_user = await db.execute(select(User).filter(User.id == user_id))
    db_user = db_user.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    await db.delete(db_user)
    await db.commit()   
    return db_user


@router.post("/posts/", response_model=PostInDB)
async def create_post(post: PostCreate, user_id: int, db: db):
    db_post = Post(title=post.title, content=post.content, user_id=user_id)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

@router.get("/posts/{post_id}", response_model=PostInDB)
async def get_post(post_id: int, db: db):
    result = await db.execute(select(Post).filter(Post.id == post_id))
    db_post = result.scalar_one_or_none()
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return db_post

@router.get("/posts/", response_model=list[PostInDB])
async def get_posts(db: db, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Post).offset(skip).limit(limit))
    return result.scalars().all()


@router.put("/posts/{post_id}", response_model=PostInDB)
async def update_post_put(post_id: int, post: PostPut, db: db):
    db_post = await db.execute(select(Post).filter(Post.id == post_id))
    db_post = db_post.scalar_one_or_none()
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    db_post.title = post.title
    db_post.content = post.content

    await db.commit()
    await db.refresh(db_post)
    return db_post

@router.patch("/posts/{post_id}", response_model=PostInDB)
async def update_post_patch(post_id: int, post: PostPatch, db: db):
    db_post = await db.execute(select(Post).filter(Post.id == post_id))
    db_post = db_post.scalar_one_or_none()
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post.title:
        db_post.title = post.title
    if post.content:
        db_post.content = post.content
    await db.commit()
    await db.refresh(db_post)
    return db_post

@router.delete("/posts/{post_id}", response_model=PostInDB)
async def delete_post(post_id: int, db: db):
    db_post = await db.execute(select(Post).filter(Post.id == post_id))
    db_post = db_post.scalar_one_or_none()
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    await db.delete(db_post)
    await db.commit()
    return db_post