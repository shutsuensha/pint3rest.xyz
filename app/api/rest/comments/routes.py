import json
import uuid

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from pydantic import ValidationError
from sqlalchemy import func, insert, select, update

from app.api.rest.dependencies import db, filter, user_id
from app.api.rest.utils import save_file
from app.config import settings
from app.postgresql.models import CommentsOrm, PinsOrm

from app.celery.tasks import make_update_comment_pin, make_update_reply_comment

from .schemas import CommentIn, CommentOut

import mimetypes

mimetypes.add_type('image/webp', '.webp')

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/{pin_id}", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
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

    if pin.user_id != user_id:
        make_update_comment_pin.delay(pin.user_id, user_id, pin.id, comment.id)
    
    return comment


@router.get("/{pin_id}", response_model=list[CommentOut])
async def get_comments_on_pin(pin_id: int, db: db, user_id: user_id, filter: filter):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
    if pin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pin not found")

    comments = await db.scalars(
        select(CommentsOrm)
        .where(CommentsOrm.pin_id == pin_id)
        .order_by(CommentsOrm.id.desc())
        .offset(filter.offset)
        .limit(filter.limit)
    )
    return comments


@router.get("/get-by-id/{comment_id}", response_model=CommentOut)
async def get_comment_by_id(comment_id: int, db: db, user_id: user_id):
    comment = await db.scalar(
        select(CommentsOrm)
        .where(CommentsOrm.id == comment_id)
    )
    return comment


@router.get("/cnt/comments/{pin_id}")
async def get_cnt_comments_on_pin(pin_id: int, db: db, user_id: user_id):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
    if pin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pin not found")

    cnt_comments = await db.scalar(
        select(func.count()).select_from(CommentsOrm).where(CommentsOrm.pin_id == pin_id)
    )
    return cnt_comments


@router.get("/cnt/replies/{comment_id}")
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
    image_path = f"{settings.MEDIA_PATH}comments/{unique_filename}"
    await save_file(file.file, image_path)

    comment = await db.scalar(
        update(CommentsOrm)
        .where(CommentsOrm.id == id)
        .values(image=image_path)
        .returning(CommentsOrm)
    )
    await db.commit()

    return comment


@router.get("/upload/{id}")
async def get_image(user_id: user_id, id: int, db: db):
    comment = await db.scalar(select(CommentsOrm).where(CommentsOrm.id == id))
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="comment not found")

    mime_type, _ = mimetypes.guess_type(comment.image)
    
    # Если MIME тип не определен, принудительно задаем для WebP

    if mime_type is None:
        if comment.image.endswith('.webp'):
            mime_type = 'image/webp'
        else:
            mime_type = 'application/octet-stream'

    return FileResponse(comment.image, media_type=mime_type)


@router.post(
    "/comment/{comment_id}", response_model=CommentOut, status_code=status.HTTP_201_CREATED
)
async def create_comment_on_comment(
    comment_id: int, db: db, user_id: user_id, comment_model: CommentIn
):
    comment = await db.scalar(select(CommentsOrm).where(CommentsOrm.id == comment_id))
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="comment not found")

    reply_comment = await db.scalar(
        insert(CommentsOrm)
        .values(content=comment_model.content, comment_id=comment_id, user_id=user_id)
        .returning(CommentsOrm)
    )
    await db.commit()

    if comment.user_id != user_id:
        make_update_reply_comment.delay(comment.user_id, user_id, comment.pin_id, comment.id, reply_comment.id)
    return reply_comment


@router.get("/comment/{comment_id}", response_model=list[CommentOut])
async def get_comments_on_comment(comment_id: int, db: db, user_id: user_id, filter: filter):
    comment = await db.scalar(select(CommentsOrm).where(CommentsOrm.id == comment_id))
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="comment not found")

    comments = await db.scalars(
        select(CommentsOrm)
        .where(CommentsOrm.comment_id == comment_id)
        .order_by(CommentsOrm.id.desc())
        .offset(filter.offset)
        .limit(filter.limit)
    )
    return comments


@router.post(
    "/create-comment-on-pin-entity/{pin_id}",
    response_model=CommentOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment_on_pin_entity(
    pin_id: int,
    db: db,
    user_id: user_id,
    comment_model: str = Form(...),
    file: UploadFile = File(...),
):
    
    ALLOWED_FILE_TYPES = ['image/jpeg', 'image/jpg', 'image/gif', 'image/webp', 'image/png', 'image/bmp', 'video/mp4', 'video/webm']
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=415, detail="Invalid file type. Allowed types: .jpg, .jpeg, .gif, .webp, .png, .bmp, .mp4, .webm")
    
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
    if pin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pin not found")

    try:
        comment_model = json.loads(comment_model)
        comment_model = CommentIn(**comment_model)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {e.errors()}")

    comment = await db.scalar(
        insert(CommentsOrm)
        .values(content=comment_model.content, pin_id=pin_id, user_id=user_id)
        .returning(CommentsOrm)
    )

    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    image_path = f"{settings.MEDIA_PATH}comments/{unique_filename}"
    await save_file(file.file, image_path)

    comment = await db.scalar(
        update(CommentsOrm)
        .where(CommentsOrm.id == comment.id)
        .values(image=image_path)
        .returning(CommentsOrm)
    )

    await db.commit()

    if pin.user_id != user_id:
        make_update_comment_pin.delay(pin.user_id, user_id, pin.id, comment.id)

    return comment


@router.post(
    "/create-comment-on-comment-entity/{comment_id}",
    response_model=CommentOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment_on_comment_entity(
    comment_id: int,
    db: db,
    user_id: user_id,
    comment_model: str = Form(...),
    file: UploadFile = File(...),
):
    
    ALLOWED_FILE_TYPES = ['image/jpeg', 'image/jpg', 'image/gif', 'image/webp', 'image/png', 'image/bmp', 'video/mp4', 'video/webm']
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=415, detail="Invalid file type. Allowed types: .jpg, .jpeg, .gif, .webp, .png, .bmp, .mp4, .webm")
    
    comment = await db.scalar(select(CommentsOrm).where(CommentsOrm.id == comment_id))
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="comment not found")

    try:
        comment_model = json.loads(comment_model)
        comment_model = CommentIn(**comment_model)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {e.errors()}")

    reply_comment = await db.scalar(
        insert(CommentsOrm)
        .values(content=comment_model.content, comment_id=comment_id, user_id=user_id)
        .returning(CommentsOrm)
    )

    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    image_path = f"{settings.MEDIA_PATH}comments/{unique_filename}"
    await save_file(file.file, image_path)

    reply_comment = await db.scalar(
        update(CommentsOrm)
        .where(CommentsOrm.id == reply_comment.id)
        .values(image=image_path)
        .returning(CommentsOrm)
    )

    await db.commit()

    if comment.user_id != user_id:
        make_update_reply_comment.delay(comment.user_id, user_id, comment.pin_id, comment.id, reply_comment.id)
    return reply_comment
