from typing import Annotated
from decimal import Decimal
from pydantic import BaseModel, Field
import uuid


class Product(BaseModel):
    id: Annotated[uuid.UUID, Field(default=uuid.uuid4(), description="`id` of the product")]
    display_name: str = Field(min_length=1, description="Human Friendly Product Name")
    product_description: str = Field(min_length=1, max_length= 240, description="Detailed description of the product")
    unit_price: Annotated[Decimal, Field(strict=True, max_digits=10, decimal_places=2, description="Unit Price of product")]
    quantity_in_stock: Annotated[int, Field(gt=0, le=1*10**6, default=1, description="Amount of product in stock")]

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