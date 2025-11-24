# Holds schemas for all users 

from pydantic import BaseModel, EmailStr, Field, field_validator
from fastapi import HTTPException, status


class UserBase(BaseModel):
    first_name: str = Field(max_length=100, min_length=2)
    last_name: str = Field(max_length=100, min_length=2)
    display_name: str | None = None
    email_address: EmailStr

    def model_post_init(self, context):
        if not self.display_name:
            self.display_name = self.first_name + " " + self.last_name
    

class UserIn(UserBase):
    password: str = Field(min_length=12, max_length=100)

    @field_validator("password")
    def validate_password(cls,p:str) -> str:
        if p.lower() == p:
            raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail="Password must contain an uppercase letter")
        if not any(c in "!@#$&*()" for c in p):
            raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail="Password must contain one of the following special characters: !@#$&*()")
        if not any(c.isdigit() for c in p):
            raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail="Password must include at least one number")
        #if any(" " in p):
            #raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail="Password cannot contain any spaces")
        
        return p

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "email_address": "jane.doe@example.com",
                    "password": "StrongP@assword1"

                }
                
            ]
        }
    
    }

class UserOut(UserBase):
    message: str = "User created successfully"

