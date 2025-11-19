from fastapi import APIRouter, Path, Body
from typing import Annotated
from schemas.users import UserIn, UserOut

router = APIRouter()

fake_database = {}





@router.post("/user/create-user", tags=["user"], summary="Create a user record in the database",response_model=UserOut)
async def create_user(user_info: UserIn):
    data = user_info.model_dump()
    email_address = data.pop("email_address")

    fake_database[email_address] = data

    return user_info

    
