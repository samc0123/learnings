from fastapi import APIRouter, Path, Body
from typing import Annotated
from schemas.users import UserIn, UserOut
import json
import os


router = APIRouter()

fake_database_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'fake_database.json'))







@router.post("/user/create-user", tags=["user"], summary="Create a user record in the database",response_model=UserOut)
async def create_user(user_info: UserIn):
    data = user_info.model_dump()
    email_address = data.pop("email_address")

    try:
        with open(fake_database_path,'r') as f:
            fake_database: dict = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        fake_database = {}
        
    if email_address in fake_database:
        fake_database[email_address].update(data)
    else:
        fake_database[email_address] = data
    with open(fake_database_path,'w') as f:
        json.dump(fake_database, f)
    f.close()
    

    return user_info

    
