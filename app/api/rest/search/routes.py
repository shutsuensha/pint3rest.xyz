from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from app.api.rest.dependencies import db, user_id
from sqlalchemy import select, delete
from app.postgresql.models import SearchOrm, UsersOrm
from .schemas import SearchQueryModel


router = APIRouter(prefix="/search", tags=["search"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_query_search(queryModel: SearchQueryModel, db: db, user_id: user_id):
    # Проверяем, есть ли уже такой запрос у пользователя
    existing_query = await db.execute(
        select(SearchOrm).where(SearchOrm.user_id == user_id, SearchOrm.query == queryModel.query)
    )
    if existing_query.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Query already exists")

    # Если нет, добавляем
    new_search = SearchOrm(user_id=user_id, query=queryModel.query)
    db.add(new_search)
    await db.commit()


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_query_search(queryModel: SearchQueryModel, user_id: user_id, db: db):
    query_stmt = (
        select(SearchOrm)
        .where(SearchOrm.user_id == user_id, SearchOrm.query == queryModel.query)
    )
    result = await db.execute(query_stmt)
    search_entry = result.scalar_one_or_none()

    if not search_entry:
        raise HTTPException(status_code=404, detail="Query not found")

    await db.delete(search_entry)
    await db.commit()


@router.get("/latest", response_model=list[str])
async def get_latest_searches(user_id: user_id, db: db):
    query = (
        select(SearchOrm.query)
        .where(SearchOrm.user_id == user_id)
        .order_by(SearchOrm.created_at.desc())  # Сортируем по дате (от новых к старым)
        .limit(5)  # Ограничиваем до 5 записей
    )
    result = await db.execute(query)
    return result.scalars().all()
