from fastapi import APIRouter, status, HTTPException, Path
import os, json, uuid
from schemas.products import Product,ProductUpdate
from models.database_operations import get_database_information, write_database_information
from typing import Annotated

router = APIRouter()

fake_database_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'fake_database_products.json'))
fake_database_path_product_names = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'fake_database_product_names.json'))

@router.post("/products/create", tags=["products"], summary="Create product entry", description="Register product, including the name, amount in stock, price, etc.", response_model=Product)
async def create_product(data:Product):


    existing_product_names = get_database_information(fake_database_path=fake_database_path_product_names)

    if existing_product_names.get(data.display_name) is not None:
        product_id = existing_product_names.get(data.display_name).get("id")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product already exists. Please use `/get` route with id: {product_id}")
    
    else:

        # Write the product to the product database
        fake_database = get_database_information(fake_database_path=fake_database_path)
        product_id= str(uuid.uuid4())
        data.id = product_id # For return to client
        data.unit_price = float(data.unit_price)
        fake_database[product_id] = data.model_dump()

    
        write_database_information(database_information=fake_database, fake_database_path=fake_database_path)

        # Register the display name to the display names database 
        fake_database_product_names = get_database_information(fake_database_path=fake_database_path_product_names)
        fake_database_product_names[data.display_name] = {
            "id":product_id
        }

        write_database_information(database_information=fake_database_product_names, fake_database_path=fake_database_path_product_names)

        
    return data


@router.get("/products/get/{id}", tags=["products"], summary="Get product information", description="Retrieve price, quantity in stock, and other info", response_model=Product)
async def get_product(id:Annotated[str, Path(title="ID of item to get")]):

    fake_database = get_database_information(fake_database_path=fake_database_path)

    if fake_database.get(id) is not None:
        return Product(**fake_database.get(id))
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    # ---- Placeholder --- #
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

async def update_product_availability(data:ProductUpdate):
    '''
    Update the product inventory up or down depending on purchases. Internal route only
    '''
    #TODO: Make this route internal accessible only, for now fine as is 


    fake_database = get_database_information(fake_database_path=fake_database_path)

    # Validator already ran, so we first remove then add stock
    stock = fake_database[data.product_id].get("quantity_in_stock")
    if data.inventory_to_remove is not None:
        stock -= data.inventory_to_remove
    if data.inventory_to_add is not None:
        stock += data.inventory_to_add
    fake_database[data.product_id]["quantity_in_stock"] = stock
    
    return Product(**fake_database.get(data.product_id))

    # --- Placeholder --- # 
    return Product(
        id=uuid.uuid4(),
        display_name="Test product",
        product_description=" This is a test product", 
        unit_price= 1.23,
        quantity_in_stock= 5
    )