from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pymongo import ReturnDocument

from app.mongodb.database import mongo

from .schemas import UserIn, UserInPatch, UserOut

router = APIRouter(prefix="/mongodb", tags=["users-mongodb"])


@router.post("/users/", response_model=UserOut)
async def create_user(user: UserIn):
    users_collection = mongo.get_collection("users")
    new_user = user.model_dump()
    result = await users_collection.insert_one(new_user)
    new_user["id"] = str(result.inserted_id)
    return new_user


@router.get("/users/", response_model=list[UserOut])
async def get_users():
    users_collection = mongo.get_collection("users")
    users = await users_collection.find().to_list(100)
    return [{"id": str(user["_id"]), **user} for user in users]


@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: str):
    users_collection = mongo.get_collection("users")
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "age": user["age"],
    }


@router.put("/users/{user_id}", response_model=UserOut)
async def update_user_put(user_id: str, user_in: UserIn):
    users_collection = mongo.get_collection("users")

    updated_user = await users_collection.find_one_and_update(
        {"_id": ObjectId(user_id)},  # Find user by ID
        {"$set": user_in.model_dump()},  # Update fields
        return_document=ReturnDocument.AFTER,  # Return updated document
    )

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": str(updated_user["_id"]),
        "name": updated_user["name"],
        "email": updated_user["email"],
        "age": updated_user["age"],
    }


@router.patch("/users/{user_id}", response_model=UserOut)
async def update_user_patch(user_id: str, user_in: UserInPatch):
    users_collection = mongo.get_collection("users")

    updated_user = await users_collection.find_one_and_update(
        {"_id": ObjectId(user_id)},  # Find user by ID
        {"$set": user_in.model_dump(exclude_unset=True)},  # Update fields
        return_document=ReturnDocument.AFTER,  # Return updated document
    )

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": str(updated_user["_id"]),
        "name": updated_user["name"],
        "email": updated_user["email"],
        "age": updated_user["age"],
    }


@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    users_collection = mongo.get_collection("users")
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
