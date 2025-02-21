from fastapi import APIRouter


router = APIRouter(prefix="/users/mongodb", tags=["users-mongodb"])


# @router.post("/users/", response_model=UserInResponse)
# async def create_user(user: User):
#     users_collection = mongo.get_collection("users")
#     new_user = {
#         "name": user.name,
#         "email": user.email,
#         "age": user.age
#     }
#     result = await users_collection.insert_one(new_user)
#     new_user["id"] = str(result.inserted_id)  # Convert ObjectId to string
#     return new_user

# # Get users (R)
# @router.get("/users/", response_model=List[UserInResponse])
# async def get_users():
#     users_collection = mongo.get_collection("users")
#     users = await users_collection.find().to_list(100)
#     return [{"id": str(user["_id"]), **user} for user in users]

# # Get user by ID (R)
# @router.get("/users/{user_id}", response_model=UserInResponse)
# async def get_user(user_id: str):
#     users_collection = mongo.get_collection("users")
#     user = await users_collection.find_one({"_id": ObjectId(user_id)})
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return {"id": str(user["_id"]), "name": user["name"], "email": user["email"], "age": user["age"]}

# # Update a user (U)
# @router.put("/users/{user_id}", response_model=UserInResponse)
# async def update_user(user_id: str, user: User):
#     users_collection = mongo.get_collection("users")
#     update_data = {key: value for key, value in user.dict().items() if value is not None}
#     result = await users_collection.update_one(
#         {"_id": ObjectId(user_id)}, 
#         {"$set": update_data}
#     )
#     if result.matched_count == 0:
#         raise HTTPException(status_code=404, detail="User not found")
#     updated_user = await users_collection.find_one({"_id": ObjectId(user_id)})
#     return {"id": str(updated_user["_id"]), "name": updated_user["name"], "email": updated_user["email"], "age": updated_user["age"]}

# # Delete a user (D)
# @router.delete("/users/{user_id}")
# async def delete_user(user_id: str):
#     users_collection = mongo.get_collection("users")
#     result = await users_collection.delete_one({"_id": ObjectId(user_id)})
#     if result.deleted_count == 0:
#         raise HTTPException(status_code=404, detail="User not found")
#     return {"message": "User deleted successfully"}