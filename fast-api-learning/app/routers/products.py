from fastapi import APIRouter, status, HTTPException, Path
import os, json, uuid
from schemas.products import Product,ProductUpdate
from models.database_operations import get_database_information, write_database_information

router = APIRouter()


@router.post("/products/create", tags=["products"], summary="Create product entry", description="Register product, including the name, amount in stock, price, etc.", response_model=Product)
async def create_product(data:Product):
    return data


@router.get("products/get/{id}", tags=["products"], summary="Get product information", description="Retrieve price, quantity in stock, and other info", response_model=Product)
async def get_product(id:str):
    return Product(
        id=uuid.uuid4(),
        display_name="Test product",
        product_description=" This is a test product", 
        unit_price= 1.23,
        quantity_in_stock= 5
    )

@router.put("/products/update-inventory/{id}", tags=["products"], summary="Update product stock", \
            description= "Add or remove inventory from the product. DOES NOT create a product if `id` is invalid/not found", \
                response_model=Product)

async def update_product(data:ProductUpdate):
    return Product(
        id=uuid.uuid4(),
        display_name="Test product",
        product_description=" This is a test product", 
        unit_price= 1.23,
        quantity_in_stock= 5
    )