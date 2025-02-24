from fastapi import APIRouter, Response, status, HTTPException
from .schemas import PinOut, PinIn
from .cache import pins_cache_key, clear_all_pins_cache, disable_client_cache
from fastapi_cache.decorator import cache
from app.api.rest.dependencies import user_id, db, filter
from sqlalchemy import select, desc, insert, delete
from app.postgresql.models import PinsOrm


router = APIRouter(prefix="/pins/cache", tags=["pins-cache"])


@router.get('/', response_model=list[PinOut])
@cache(expire=300, key_builder=pins_cache_key)
async def get_pins(user_id: user_id, db: db, filter: filter, response: Response):

    disable_client_cache(response)
    
    pins = await db.scalars(
        select(PinsOrm)
        .offset(filter.offset)
        .limit(filter.limit)
        .order_by(desc(PinsOrm.id))
    )

    return [PinOut.model_validate(vars(el)) for el in pins]



@router.post('/', response_model=PinOut, status_code=status.HTTP_201_CREATED)
async def create_pin(user_id: user_id, db: db, pin_model: PinIn):
    pin = await db.scalar(
        insert(PinsOrm)
        .values(**pin_model.model_dump(), user_id=user_id)
        .returning(PinsOrm)
    )
    await db.commit()
    await clear_all_pins_cache()
    return pin


@router.delete('/{pin_id}', status_code=status.HTTP_204_NO_CONTENT)
async def user_delete_created_pin(pin_id: int, user_id: user_id, db: db):
    pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
    if pin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pin not found")

    await db.execute(delete(PinsOrm).where(PinsOrm.user_id == user_id, PinsOrm.id == pin_id))
    await db.commit()
    await clear_all_pins_cache()
    return {'status', 'ok'}