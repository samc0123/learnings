from typing import Annotated, Optional
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator
import uuid
import json
import os
from fastapi import HTTPException, status

class Product(BaseModel):
    id: Annotated[uuid.UUID, Field(default=uuid.uuid4(), description="`id` of the product")]
    display_name: str = Field(min_length=1, description="Human Friendly Product Name")
    product_description: str = Field(min_length=1, max_length= 240, description="Detailed description of the product")
    unit_price: Annotated[Decimal, Field(strict=True, max_digits=10, decimal_places=2, description="Unit Price of product")]
    quantity_in_stock: Annotated[int, Field(gt=0, le=1*10**4, default=1, description="Amount of product in stock")]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                   "display_name": "Cocoa Puffs",
                   "product_description":"A top-tier cereal, but not in the level of Cinnamon Toast Crunch",
                   "unit_price":2.99
                }
                
            ]
        }
    }

class ProductUpdate:
    inventory_to_add: Annotated[Optional[int], Field(gt=0, le=1*10**4 - 1, description="Amount of product to add to inventory")]
    inventory_to_remove: Annotated[Optional[int], Field(gt=0, le=1*10**4 - 1, description="Amount of product to remove from inventory.")]
    product_id: Annotated[uuid.UUID, Field(description="`id` value of the product")]

    #TODO: Get this method to return correctly
    @classmethod
    def check_inventory(product_id:str, val:int, operation:str):
        fake_database_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'fake_database_products.json'))

        try:
            with open(fake_database_path,'r') as f:
                fake_database: dict = json.load(f)

                match operation:
                    case "add":
                        if fake_database.get(product_id) is not None and fake_database.get(product_id) + val <= 1*10**4:
                            return val
                        else:
                            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Either product doesn't exist or the value is too large to be stored in inventory. Please try again")
                    case "remove":
                        if fake_database.get(product_id) is not None and fake_database.get(product_id) - val >= 0:
                            return val
                        else:
                            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Either product doesn't exist or there is not enough inventory. Please try again")
                    case _ :
                        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Not a valid check attribute")
        except (FileNotFoundError, json.JSONDecodeError):
            fake_database = {}
            return val # No inventory created yet, so only Field level validators needed 
            
        

        
        
    @field_validator("inventory_to_add")
    def check_inventory(cls,v):
        #TODO: return cls.check_inventory(pr) 
        pass
    