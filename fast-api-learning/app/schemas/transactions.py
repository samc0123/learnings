# Holds classes for all transaction objects

from pydantic import BaseModel, EmailStr, Field, field_validator
from fastapi import HTTPException, status
from typing import Annotated, Optional
import uuid
from decimal import Decimal


class TransactionBase(BaseModel):
    product_id: Annotated[uuid.UUID, Field(description="`id` object of product in system")]
    quantity: Annotated[int, Field(gt=0, le= 1*10**4, description="Quantity of product in inventory")]

class TransactionIn(TransactionBase):
    email: Annotated[EmailStr, Field(description="Email ID (and unique `email` identifier) of user making the transaction")]


    model_config ={
        "json_schema_extra": {
            "examples": [
                {
                   "product_id": "9f0c3e4b-2d8a-47b9-9c1f-0e8b52d3a4f2",
                    "quantity": 5, 
                    "email": "test@example.com"
                }
                
            ]
        }
    }

class TransactionOut(TransactionBase):
    product_name: Annotated[str, Field(description="`display_name` attribute of the product")]
    price: Annotated[Decimal, Field(gt=0.01, max_digits=10, decimal_places=2, description="Cost of the transaction to the user")]
    transaction_id: Annotated[Optional[uuid.UUID], Field(description="`id` of the transaction stored in database")]

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