from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(prefix="/httpx", tags=["users-httpx"])

BASE_URL = "https://jsonplaceholder.typicode.com"


@router.get("/users/")
async def get_users():
    """Fetches a list of users."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/users")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Ошибка при получении пользователей")
        return response.json()


@router.get("/users/{user_id}")
async def get_user(user_id: int):
    """Fetches a specific user by ID."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/users/{user_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Пользователь не найден")
        return response.json()


@router.post("/users/")
async def create_user(user_data: dict):
    """Creates a new user."""
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/users", json=user_data)
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail="Ошибка при создании пользователя")
        return response.json()


@router.put("/users/{user_id}")
async def update_user(user_id: int, user_data: dict):
    """Updates an existing user."""
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{BASE_URL}/users/{user_id}", json=user_data)
        if response.status_code not in {200, 204}:
            raise HTTPException(status_code=response.status_code, detail="Ошибка при обновлении пользователя")
        return response.json()


@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """Deletes a user by ID."""
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/users/{user_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Ошибка при удалении пользователя")
        return {"message": "Пользователь удален"}
