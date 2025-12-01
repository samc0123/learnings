from fastapi import APIRouter, Path, Body, HTTPException, status, Response
from typing import Dict
from schemas.users import UserIn, UserOut
import os
from models.database_operations import get_database_information, write_database_information


router = APIRouter()

fake_database_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'fake_database_users.json'))





@router.post("/user/create-user", tags=["user"], summary="Create a user record in the database",response_model=UserOut)
async def create_user(user_info: UserIn):
    data = user_info.model_dump()
    email_address = str(data.pop("email_address")).lower()

    
    fake_database = get_database_information(fake_database_path=fake_database_path)
    if email_address in fake_database:
        fake_database[email_address].update(data)
    else:
        fake_database[email_address] = data
    

    write_database_information(database_information=fake_database, fake_database_path=fake_database_path)
    

    return user_info


@router.put("/user/update/{email}", tags=["user"], summary="Update User Information",description="Update user information via email. If email is updated, remove old record and create new one", response_model=UserOut)
async def update_user_information(user_info:UserIn, email:str):
    # Step 0: Retrieve user information from fake database
    fake_database = get_database_information(fake_database_path=fake_database_path)

    email = email.lower()
    current_user_info = fake_database.get(email) 
    if current_user_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    data = user_info.model_dump()
    new_email = data.pop("email_address")

    # Case 1: Change in email address, means new record must be created
    if user_info.email_address != email:
        # Step 1: Remove existing record 
        del fake_database[email]


        fake_database[new_email] = data
        write_database_information(database_information=fake_database, fake_database_path=fake_database_path)

    # Case 2: Email is the same, then just update the data by removing the email address
    else:

        fake_database[email].update(data)
        write_database_information(database_information=fake_database, fake_database_path=fake_database_path)
    response = UserOut(**data, email_address=new_email, message="User Updated successfully")
    return response

@router.delete("/user/remove/{email}", tags=["user"], summary="Remove user record from system", description="Remove user via `email` identifier")
async def remove_user(email:str):
    # Step 0: Retrieve user information from fake database
    fake_database = get_database_information(fake_database_path=fake_database_path)
    

    email = email.lower()
    if fake_database.get(email) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        del fake_database[email]
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/user/get/{email}", tags= ["user"], summary="Get User Information", description="Retrieve user information and confirm existence", response_model=UserOut)
async def get_user(email:str):
    fake_database = get_database_information(fake_database_path=fake_database_path)

    email = email.lower()

    if fake_database.get(email) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        data = fake_database.get(email)
        return UserOut(**data, email_address=email, message= None)
