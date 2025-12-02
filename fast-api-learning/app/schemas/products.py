from typing import Annotated, Optional
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator, model_validator
import uuid
import json
import os
from fastapi import HTTPException, status
from models.database_operations import get_database_information

class Product(BaseModel):
    id: Annotated[Optional[str], Field(default= None, description="`id` of the product")]
    display_name: Annotated[str, Field(min_length=1, description="Human Friendly Product Name")]
    product_description: Annotated[str, Field(min_length=1, max_length= 240, description="Detailed description of the product")]
    unit_price: Annotated[Decimal, Field(max_digits=10, decimal_places=2, description="Unit Price of product")]
    quantity_in_stock: Annotated[int, Field(gt=0, le=1*10**4, default=1, description="Amount of product in stock")]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                   "display_name": "Cocoa Puffs",
                   "product_description":"A top-tier cereal, but not in the level of Cinnamon Toast Crunch",
                   "unit_price": "2.99", 
                   "quantity_in_stock": 5
                }
                
            ]
        }
    }

class ProductUpdate(BaseModel):
    inventory_to_add: Annotated[Optional[int], Field(default= 0, gt=-1, le=1*10**4 - 1, description="Amount of product to add to inventory")]
    inventory_to_remove: Annotated[Optional[int], Field(default=0, gt=-1, le=1*10**4 - 1, description="Amount of product to remove from inventory.")]
    product_id: Annotated[str, Field(description="`id` value of the product")]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                   "inventory_to_add": 7,
                   "product_id": "e9b1f3c7-04bb-4e0f-9dff-315beffb2a36"
                }, 
                {
                   "inventory_to_remove": 12,
                   "product_id": "d5b7a1fb-3c8a-4eab-8cd2-7f6c9b0c6f91"
                }, 
                {
                    "inventory_to_add": 15, 
                    "inventory_to_remove": 18, 
                    "product_id": "4c3f0b8e-1b6c-4c1b-8a6e-2f0e5e4b9d77"
                }
                
            ]
        }
    }

    #TODO: Get this method to return correctly
    @classmethod
    def check_inventory(cls,product_id:str, val:int, operation:str):
        fake_database_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'fake_database_products.json'))

        try:
            with open(fake_database_path,'r') as f:
                fake_database = get_database_information(fake_database_path=fake_database_path)

                match operation:
                    case "add":
                        if fake_database.get(product_id) is not None and fake_database.get(product_id).get("quantity_in_stock") + val <= 1*10**4:
                            return val
                        else:
                            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Either product doesn't exist or the value is too large to be stored in inventory. Please try again")
                    case "remove":
                        if fake_database.get(product_id) is not None and fake_database.get(product_id).get("quantity_in_stock") - val >= 0:
                            return val
                        else:
                            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Either product doesn't exist or there is not enough inventory. Please try again")
                    case _ :
                        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Not a valid check attribute")
        except (FileNotFoundError, json.JSONDecodeError):
            fake_database = {}
            return val # No inventory created yet, so only Field level validators needed 
            
        

        
        
    @model_validator(mode='after')
    def validate_inventory(self):
        if self.inventory_to_add is not None:
            return self.check_inventory(self.product_id,self.inventory_to_add,"add")
        if self.inventory_to_remove is not None:
            return self.check_inventory(self.product_id,self.inventory_to_remove,"remove")

        return self
    
    
    