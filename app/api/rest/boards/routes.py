from fastapi import APIRouter, HTTPException, status
from .schemas import BoardCreate, BoardResponse
from app.api.rest.dependencies import db, user_id, filter
from app.postgresql.models import BoardsOrm, PinsOrm, board_pins,UsersOrm
from sqlalchemy import select, update, insert, delete
from typing import Optional
from app.api.rest.pins.schemas import PinOut

router = APIRouter(prefix="/boards", tags=["boards"])


@router.post("/", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
async def create_board(board: BoardCreate, db: db, user_id: user_id):
    new_board = BoardsOrm(user_id=user_id, title=board.title)
    db.add(new_board)
    await db.commit()
    await db.refresh(new_board)
    return new_board


@router.patch("/selected", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_board_selected(db: db, user_id: user_id, board_id: int):
    user = await db.scalar(
        update(UsersOrm).where(UsersOrm.id == user_id).values(selected_board=board_id).returning(UsersOrm)
    )
    await db.commit()

@router.patch("/selected/disable", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_board_selected(db: db, user_id: user_id):
    user = await db.scalar(
        update(UsersOrm).where(UsersOrm.id == user_id).values(selected_board=None).returning(UsersOrm)
    )
    await db.commit()


@router.get("/selected", response_model=Optional[BoardResponse])
async def get_user_selected_board(db: db, user_id: user_id):
    stmt = (
        select(BoardsOrm)
        .join(UsersOrm, UsersOrm.selected_board == BoardsOrm.id)
        .where(UsersOrm.id == user_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none() 



@router.get("/user/{id}", response_model=list[BoardResponse])
async def get_user_boards(id:int, db: db, user_id: user_id):
    result = await db.execute(select(BoardsOrm).where(BoardsOrm.user_id == id))
    boards = result.scalars().all()
    return boards

@router.get("/me", response_model=list[BoardResponse])
async def get_me_user_boards(db: db, user_id: user_id):
    result = await db.execute(select(BoardsOrm).where(BoardsOrm.user_id == user_id))
    boards = result.scalars().all()
    return boards


@router.post("/{board_id}/pins/{pin_id}")
async def add_pin_to_board(board_id: int, pin_id: int, db: db, user_id: user_id):
    """Добавляет пин в доску."""
    # Проверяем, существует ли доска и пин
    board_exists = await db.execute(select(BoardsOrm).where(BoardsOrm.id == board_id))
    pin_exists = await db.execute(select(PinsOrm).where(PinsOrm.id == pin_id))
    if not board_exists.scalar() or not pin_exists.scalar():
        raise HTTPException(status_code=404, detail="Board or Pin not found")
    
    # Проверяем, существует ли уже такая связка
    existing_link = await db.execute(select(board_pins).where((board_pins.c.board_id == board_id) & (board_pins.c.pin_id == pin_id)))
    if existing_link.scalar():
        raise HTTPException(status_code=409, detail="Pin is already in the board")

    # Добавляем связь между доской и пином
    stmt = insert(board_pins).values(board_id=board_id, pin_id=pin_id)
    await db.execute(stmt)
    await db.commit()
    return {"message": "Pin added to board"}


@router.delete("/{board_id}/pins/{pin_id}")
async def remove_pin_from_board(board_id: int, pin_id: int, db: db, user_id: user_id):
    """Удаляет пин из доски."""
    stmt = delete(board_pins).where((board_pins.c.board_id == board_id) & (board_pins.c.pin_id == pin_id))
    result = await db.execute(stmt)
    await db.commit()
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Pin not found in board")
    
    return {"message": "Pin removed from board"}



@router.get("/{board_id}", response_model=list[PinOut])
async def get_pins_by_boardg(board_id: int, user_id: user_id, db: db, filter: filter):
    result = await db.execute(select(board_pins).where(board_pins.c.board_id == board_id))
    rows = result.all()
    pins = []
    for row in rows:
        pin_id = row[1]
        pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == pin_id))
        pins.append(pin)
    return pins[filter.offset : filter.offset + filter.limit]


@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_board(board_id: int, db: db, user_id: user_id):
    # Ищем доску по ID
    board = await db.execute(select(BoardsOrm).where(BoardsOrm.id == board_id, BoardsOrm.user_id == user_id))
    board = board.scalars().first()

    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")

    # Удаляем доску
    await db.delete(board)
    await db.commit()
    
    return {"message": "Board deleted successfully"}