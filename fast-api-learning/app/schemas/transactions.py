# Holds classes for all transaction objects

from pydantic import BaseModel, EmailStr, Field, field_validator
from fastapi import HTTPException, status
from typing import Annotated, Optional
import uuid
from decimal import Decimal


class TransactionBase(BaseModel):
    
    quantity: Annotated[int, Field(gt=0, le= 1*10**4, description="Quantity of product in inventory")]

class TransactionIn(TransactionBase):
    email: Annotated[EmailStr, Field(description="Email ID (and unique `email` identifier) of user making the transaction")]
    product_id: Annotated[str, Field(description="`id` object of product in system")]

    model_config ={
        "json_schema_extra": {
            "examples": [
                {
                   "product_id": "a1012f76-8a85-4d7e-bcd5-dfdf09887f3e",
                    "quantity": 5, 
                    "email": "test@example.com"
                }
                
            ]
        }
    }

class TransactionOut(TransactionBase):
    product_name: Annotated[str, Field(description="`display_name` attribute of the product")]
    price: Annotated[int, Field(gt=1, description="Cost of the transaction to the user")]
    transaction_id: Annotated[Optional[str], Field(description="`id` of the transaction stored in database")]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                   "product_name":"Cocoa Pebbles",
                   "price": 2.99,
                   "transaction_id": "a77de1ff-b75d-49cc-8008-8b6168e8e846"
                }
                
            ]
        }
    }