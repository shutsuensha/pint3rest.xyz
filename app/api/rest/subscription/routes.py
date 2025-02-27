from fastapi import APIRouter, HTTPException, status
from sqlalchemy import delete, func, insert, select

from app.api.rest.dependencies import db, filter, user_id
from app.api.rest.users.schemas import UserOut
from app.postgresql.models import SubsrciptionsOrm, UsersOrm

router = APIRouter(prefix="/subscription", tags=["subscriptions"])


@router.post("/{user_id_to_follow}", status_code=status.HTTP_201_CREATED)
async def user_subscibe_user(db: db, user_id: user_id, user_id_to_follow: int):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id_to_follow))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_id == user_id_to_follow:
        raise HTTPException(status_code=409, detail="User cannot follow themselves")

    await db.execute(
        insert(SubsrciptionsOrm).values(follower_id=user_id, following_id=user_id_to_follow)
    )
    await db.commit()

    return {"status": "ok"}


@router.delete("/{user_id_to_follow}", status_code=status.HTTP_204_NO_CONTENT)
async def user_delete_subscibe_user(db: db, user_id: user_id, user_id_to_follow: int):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id_to_follow))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_id == user_id_to_follow:
        raise HTTPException(status_code=409, detail="User cannot unfollow themselves")

    await db.execute(
        delete(SubsrciptionsOrm).where(
            SubsrciptionsOrm.follower_id == user_id,
            SubsrciptionsOrm.following_id == user_id_to_follow,
        )
    )
    await db.commit()

    return {"status": "ok"}


@router.get("/check_user_follow/{user_id_to_follow}")
async def check_user_follow_user(db: db, user_id: user_id, user_id_to_follow: int):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id_to_follow))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    is_following = await db.scalar(
        select(SubsrciptionsOrm).where(
            SubsrciptionsOrm.follower_id == user_id,
            SubsrciptionsOrm.following_id == user_id_to_follow,
        )
    )
    if is_following:
        return True
    else:
        return False


@router.get("/followers/{id}", response_model=list[UserOut])
async def get_user_followers(db: db, user_id: user_id, id: int, filter: filter):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    stmt = (
        select(UsersOrm)
        .join(SubsrciptionsOrm, SubsrciptionsOrm.follower_id == UsersOrm.id)
        .where(SubsrciptionsOrm.following_id == id)
        .order_by(SubsrciptionsOrm.id.desc())
        .offset(filter.offset)
        .limit(filter.limit)
    )

    result = await db.scalars(stmt)
    return result


@router.get("/followers/cnt/{id}")
async def get_cnt_user_followers(db: db, user_id: user_id, id: int):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cnt_followers = await db.scalar(
        select(func.count())
        .select_from(SubsrciptionsOrm)
        .where(SubsrciptionsOrm.following_id == id)
    )
    return cnt_followers


@router.get("/following/{id}", response_model=list[UserOut])
async def get_user_following(db: db, user_id: user_id, id: int, filter: filter):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    stmt = (
        select(UsersOrm)
        .join(SubsrciptionsOrm, SubsrciptionsOrm.following_id == UsersOrm.id)
        .where(SubsrciptionsOrm.follower_id == id)
        .order_by(SubsrciptionsOrm.id.desc())
        .offset(filter.offset)
        .limit(filter.limit)
    )

    result = await db.scalars(stmt)
    return result


@router.get("/following/cnt/{id}")
async def get_cnt_user_following(db: db, user_id: user_id, id: int):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cnt_following = await db.scalar(
        select(func.count()).select_from(SubsrciptionsOrm).where(SubsrciptionsOrm.follower_id == id)
    )
    return cnt_following
