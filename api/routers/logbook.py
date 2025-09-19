
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..db import get_db

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello, MongoDB + FastAPI"}

@router.get("/users")
async def get_users(db: AsyncIOMotorDatabase = Depends(get_db)):
    users = []
    cursor = db["users"].find({})
    async for user in cursor:
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

@router.post("/users")
async def create_user(user: dict, db: AsyncIOMotorDatabase = Depends(get_db)):
    result = await db["users"].insert_one(user)
    return {"id": str(result.inserted_id)}

