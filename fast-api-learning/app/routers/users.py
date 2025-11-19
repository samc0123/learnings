from fastapi import APIRouter, Path
from typing import Annotated


router = APIRouter()

fake_database = [
    {
        "user_id": 1,
        "name": "Ava Reynolds",
        "email": "ava.reynolds@example.com",
        "age": 29,
        "is_active": True
    },
    {
        "user_id": 2,
        "name": "Liam Carter",
        "email": "liam.carter@example.com",
        "age": 34,
        "is_active": False
    },
    {
        "user_id": 3,
        "name": "Sophia Martinez",
        "email": "sophia.martinez@example.com",
       "age": 27,
        "is_active": True
    },
    {
        "user_id": 4,
        "name": "Noah Bennett",
        "email": "noah.bennett@example.com",
        "age": 41,
        "is_active": True
    },
    {
        "user_id": 5,
        "name": "Isabella Chen",
        "email": "isabella.chen@example.com",
        "age": 22,
        "is_active": False
    }
]



@router.get("/user/{user_id}", tags=["user"], summary="Get user information")
async def get_user_information(user_id: Annotated[int, Path(title="ID of the user to get", gt=-1,le=4)]):
    return fake_database[user_id]
    
