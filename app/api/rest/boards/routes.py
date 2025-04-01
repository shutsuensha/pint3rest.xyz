from fastapi import APIRouter, HTTPException, status
from .schemas import BoardCreate, BoardResponse, PinsAddRemove
from app.api.rest.dependencies import db, user_id
from app.postgresql.models import BoardsOrm, PinsOrm, board_pins
from sqlalchemy import select

router = APIRouter(prefix="/boards", tags=["boards"])


@router.post("/", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
async def create_board(board: BoardCreate, db: db, user_id: user_id):
    new_board = BoardsOrm(user_id=user_id, title=board.title)
    db.add(new_board)
    await db.commit()
    await db.refresh(new_board)
    return new_board


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


@router.get("/user/{id}", response_model=list[BoardResponse])
async def get_user_boards(id:int, db: db, user_id: user_id):
    result = await db.execute(select(BoardsOrm).where(BoardsOrm.user_id == id))
    boards = result.scalars().all()
    return boards


