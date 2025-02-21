from fastapi import APIRouter, HTTPException, Response, status, UploadFile
from app.api.rest.dependencies import db, user_id, filter
from app.postgresql.models import PinsOrm, LikesOrm, CommentsOrm
from .schemas import LikeOut
from sqlalchemy import select, insert, delete, func


router = APIRouter(prefix="/likes", tags=["likes"])


@router.post(
    "/pin/{pin_id}", response_model=LikeOut, status_code=status.HTTP_201_CREATED
)
async def create_like_on_pin(pin_id: int, user_id: user_id, db: db):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
    if pin is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="pin not found"
        )

    like = await db.scalar(
        insert(LikesOrm).values(user_id=user_id, pin_id=pin_id).returning(LikesOrm)
    )
    await db.commit()
    return like


@router.delete("/pin/{pin_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_like_on_pin(pin_id: int, user_id: user_id, db: db):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
    if pin is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="pin not found"
        )

    await db.execute(
        delete(LikesOrm).where(LikesOrm.pin_id == pin_id, LikesOrm.user_id == user_id)
    )
    await db.commit()

    return {"deleted": "ok"}


@router.get("/pin/user_like/{pin_id}")
async def check_user_like_on_pin(pin_id: int, user_id: user_id, db: db):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
    if pin is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="pin not found"
        )

    like = await db.scalar(
        select(LikesOrm).where(LikesOrm.user_id == user_id, LikesOrm.pin_id == pin_id)
    )
    if like:
        return True
    else:
        return False


@router.get("/pin/likes/cnt/{pin_id}")
async def get_cnt_likes_on_pin(pin_id: int, db: db, user_id: user_id):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
    if pin is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="pin not found"
        )

    cnt_likes = await db.scalar(
        select(func.count()).select_from(LikesOrm).where(LikesOrm.pin_id == pin_id)
    )
    return cnt_likes


@router.get("/pin/likes/{pin_id}", response_model=list[LikeOut])
async def get_likes_on_pin(pin_id: int, db: db, user_id: user_id, filter: filter):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
    if pin is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="pin not found"
        )

    likes = await db.scalars(
        select(LikesOrm)
        .where(LikesOrm.pin_id == pin_id)
        .order_by(LikesOrm.id.desc())
        .offset(filter.offset)
        .limit(filter.limit)
    )
    return likes


@router.post(
    "/comment/{comment_id}", response_model=LikeOut, status_code=status.HTTP_201_CREATED
)
async def create_like_on_comment(comment_id: int, user_id: user_id, db: db):
    comment = await db.scalar(select(CommentsOrm).where(CommentsOrm.id == comment_id))
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="comment not found"
        )

    like = await db.scalar(
        insert(LikesOrm)
        .values(user_id=user_id, comment_id=comment_id)
        .returning(LikesOrm)
    )
    await db.commit()
    return like


@router.delete("/comment/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_like_on_comment(comment_id: int, user_id: user_id, db: db):
    comment = await db.scalar(select(CommentsOrm).where(CommentsOrm.id == comment_id))
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="comment not found"
        )

    await db.execute(
        delete(LikesOrm).where(
            LikesOrm.comment_id == comment_id, LikesOrm.user_id == user_id
        )
    )
    await db.commit()

    return {"deleted": "ok"}


@router.get("/comment/user_like/{comment_id}")
async def check_user_like_on_comment(comment_id: int, user_id: user_id, db: db):
    comment = await db.scalar(select(CommentsOrm).where(CommentsOrm.id == comment_id))
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="comment not found"
        )

    like = await db.scalar(
        select(LikesOrm).where(
            LikesOrm.user_id == user_id, LikesOrm.comment_id == comment_id
        )
    )
    if like:
        return True
    else:
        return False


@router.get("/comment/likes/cnt/{comment_id}")
async def get_cnt_likes_on_comment(comment_id: int, db: db, user_id: user_id):
    comment = await db.scalar(select(CommentsOrm).where(CommentsOrm.id == comment_id))
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="comment not found"
        )

    cnt_likes = await db.scalar(
        select(func.count())
        .select_from(LikesOrm)
        .where(LikesOrm.comment_id == comment_id)
    )
    return cnt_likes


@router.get("/comment/likes/{comment_id}", response_model=list[LikeOut])
async def get_likes_on_comment(
    comment_id: int, db: db, user_id: user_id, filter: filter
):
    comment = await db.scalar(select(CommentsOrm).where(CommentsOrm.id == comment_id))
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="comment not found"
        )

    likes = await db.scalars(
        select(LikesOrm)
        .where(LikesOrm.comment_id == comment_id)
        .order_by(LikesOrm.id.desc())
        .offset(filter.offset)
        .limit(filter.limit)
    )
    return likes
