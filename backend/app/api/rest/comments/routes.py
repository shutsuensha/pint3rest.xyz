from fastapi import APIRouter, HTTPException, Response, status, UploadFile
from app.api.rest.dependencies import db, user_id, filter
from .schemas import CommentIn, CommentOut
from app.postgresql.models import CommentsOrm, PinsOrm
from sqlalchemy import select, insert, update, func
import uuid
from app.api.rest.utils import save_file
from fastapi.responses import FileResponse


router = APIRouter(prefix="/comments", tags=["comments"])


@router.post('/{pin_id}', response_model=CommentOut, status_code=status.HTTP_201_CREATED)  
async def create_comment_on_pin(pin_id: int, db: db, user_id: user_id, comment_model: CommentIn):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
    if pin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pin not found")
    
    comment = await db.scalar(
        insert(CommentsOrm)
        .values(content=comment_model.content, pin_id=pin_id, user_id=user_id)
        .returning(CommentsOrm)
    )
    await db.commit()
    return comment


@router.get('/{pin_id}', response_model=list[CommentOut])
async def get_comments_on_pin(pin_id: int, db: db, user_id: user_id, filter: filter):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
    if pin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pin not found")

    comments = await db.scalars(select(CommentsOrm).where(CommentsOrm.pin_id == pin_id).order_by(CommentsOrm.id.desc()).offset(filter.offset).limit(filter.limit))
    return comments


@router.get('/cnt/comments/{pin_id}')
async def get_cnt_comments_on_pin(pin_id: int, db: db, user_id: user_id):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
    if pin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pin not found")

    cnt_comments = await db.scalar(
        select(func.count()).select_from(CommentsOrm).where(CommentsOrm.pin_id == pin_id)
    )
    return cnt_comments


@router.get('/cnt/replies/{comment_id}')
async def get_cnt_replies_on_comment(comment_id: int, db: db, user_id: user_id):
    comment = await db.scalar(select(CommentsOrm).where(CommentsOrm.id == comment_id))
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="comment not found")

    cnt_comments = await db.scalar(
        select(func.count()).select_from(CommentsOrm).where(CommentsOrm.comment_id == comment_id)
    )
    return cnt_comments


@router.post("/upload/{id}", response_model=CommentOut)
async def upload_image(user_id: user_id, id: int, db: db, file: UploadFile):

    comment = await db.scalar(select(CommentsOrm).where(CommentsOrm.id == id))
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="comment not found")
    
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    image_path = f"app/media/comments/{unique_filename}"
    save_file(file.file, image_path)
    

    comment = await db.scalar(
        update(CommentsOrm)
        .where(CommentsOrm.id == id)
        .values(image = image_path)
        .returning(CommentsOrm)
    )
    await db.commit()

    return comment


@router.get("/upload/{id}")
async def get_image(user_id: user_id, id: int, db: db):
    comment = await db.scalar(select(CommentsOrm).where(CommentsOrm.id == id))
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="comment not found")
    
    return FileResponse(comment.image)


@router.post('/comment/{comment_id}', response_model=CommentOut, status_code=status.HTTP_201_CREATED)
async def create_comment_on_comment(comment_id: int, db: db, user_id: user_id, comment_model: CommentIn):
    comment = await db.scalar(select(CommentsOrm).where(CommentsOrm.id == comment_id))
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="comment not found")

    comment = await db.scalar(
        insert(CommentsOrm)
        .values(content=comment_model.content, comment_id=comment_id, user_id=user_id)
        .returning(CommentsOrm)
    )
    await db.commit()
    return comment


@router.get('/comment/{comment_id}', response_model=list[CommentOut])
async def get_comments_on_comment(comment_id: int, db: db, user_id: user_id, filter: filter):
    comment = await db.scalar(select(CommentsOrm).where(CommentsOrm.id == comment_id))
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="comment not found")

    comments = await db.scalars(select(CommentsOrm).where(CommentsOrm.comment_id == comment_id).order_by(CommentsOrm.id.desc()).offset(filter.offset).limit(filter.limit))
    return comments