from fastapi import APIRouter, HTTPException, Response, status, UploadFile
from .schemas import UserIn, UserOut
from app.api.dependencies import db, user_id
from sqlalchemy import insert, select, update
from app.database.models import UsersOrm
from app.api.utils import hash_password, verify_password, create_access_token, save_file
import uuid
from fastapi.responses import FileResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserIn, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.username == user_in.username))
    if user:
        raise HTTPException(status_code=409, detail="user already exists")
    user = await db.scalar(
        insert(UsersOrm)
        .values(username=user_in.username, hashed_password=hash_password(user_in.password))
        .returning(UsersOrm)
    )
    await db.commit()
    return user


@router.post("/login")
async def login_user(user_in: UserIn, response: Response, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.username == user_in.username))
    if not user:
        raise HTTPException(status_code=401, detail="user not found")
    if not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="password dont match")
    access_token = create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me", response_model=UserOut)
async def get_me(user_id: user_id, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id))
    return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}


@router.get("/user_id/{id}", response_model=UserOut)
async def get_user_by_id(user_id: user_id, id: int, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return user


@router.get("/user_username/{username}", response_model=UserOut)
async def get_user_by_username(user_id: user_id, username: str, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.username == username))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return user


@router.post("/upload/{id}", response_model=UserOut)
async def upload_image(user_id: user_id, id: int, db: db, file: UploadFile):

    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    image_path = f"app/media/users/{unique_filename}"
    save_file(file.file, image_path)
    

    user = await db.scalar(
        update(UsersOrm)
        .where(UsersOrm.id == id)
        .values(image=image_path)
        .returning(UsersOrm)
    )
    await db.commit()

    return user


@router.get("/upload/{id}")
async def get_image(user_id: user_id, id: int, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    
    return FileResponse(user.image)