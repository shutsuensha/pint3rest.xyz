from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
from sqlalchemy import desc, select

from app.api.rest.dependencies import db, filter, user_id
from app.postgresql.models import PinsOrm

from .schemas import PinOut

router = APIRouter(prefix="/pins/limiter", tags=["pins-limiter"])


@router.get(
    "/", response_model=list[PinOut], dependencies=[Depends(RateLimiter(times=5, seconds=60))]
)
async def get_pins(user_id: user_id, db: db, filter: filter):
    pins = await db.scalars(
        select(PinsOrm).offset(filter.offset).limit(filter.limit).order_by(desc(PinsOrm.id))
    )

    return pins
