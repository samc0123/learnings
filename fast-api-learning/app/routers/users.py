from fastapi import APIRouter, Path, Body, HTTPException, status, Response
from typing import Annotated, Dict
from schemas.users import UserIn, UserOut
import json
import os


router = APIRouter()

fake_database_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'fake_database_users.json'))

def get_database_information() -> Dict[str, Dict[str,str]]:
    '''
    Retrieve fake database information, helper method 
    '''
    

    fake_database = {}
    try:
        with open(fake_database_path,'r') as f:
            fake_database: dict = json.load(f)
            return fake_database
    except (FileNotFoundError, json.JSONDecodeError):
        print('Database empty, initializing new database')
        return fake_database

def write_database_information(database_information:dict) -> None:
    '''
    Write back to the fake database, helper method
    '''

    with open(fake_database_path,'w') as f:
        json.dump(database_information, f)
    f.close()




@router.post("/user/create-user", tags=["user"], summary="Create a user record in the database",response_model=UserOut)
async def create_user(user_info: UserIn):
    data = user_info.model_dump()
    email_address = str(data.pop("email_address")).lower()

    
    fake_database = get_database_information()
    if email_address in fake_database:
        fake_database[email_address].update(data)
    else:
        fake_database[email_address] = data
    

    write_database_information(database_information=fake_database)
    

    return user_info


@router.put("/user/update/{email}", tags=["user"], summary="Update User Information",description="Update user information via email. If email is updated, remove old record and create new one", response_model=UserOut)
async def update_user_information(user_info:UserIn, email:str):
    # Step 0: Retrieve user information from fake database
    fake_database = get_database_information()

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
        write_database_information(fake_database)

    # Case 2: Email is the same, then just update the data by removing the email address
    else:

        fake_database[email].update(data)
        write_database_information(fake_database)
    response = UserOut(**data, email_address=new_email, message="User Updated successfully")
    return response

@router.delete("/user/remove/{email}", tags=["user"], summary="Remove user record from system", description="Remove user via `email` identifier")
async def remove_user(email:str):
    # Step 0: Retrieve user information from fake database
    fake_database = get_database_information()
    

    email = email.lower()
    if fake_database.get(email) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        del fake_database[email]
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/user/get/{email}", tags= ["user"], summary="Get User Information", description="Retrieve user information and confirm existence", response_model=UserOut)
async def get_user(email:str):
    fake_database = get_database_information()

    email = email.lower()

    if fake_database.get(email) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        data = fake_database.get(email)
        return UserOut(**data, email_address=email, message= None)
