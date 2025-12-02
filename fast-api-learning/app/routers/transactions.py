# All routes related to POS transactions 
from fastapi import APIRouter, status, HTTPException
import os, json, uuid
from schemas.transactions import TransactionIn, TransactionOut
from models.database_operations import get_database_information, write_database_information
from decimal import Decimal



router = APIRouter()

#TODO: Implement Fake database and transactions routes to track POS purchases 
fake_database_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'fake_database_transactions.json'))



@router.get("/transactions/get/{id}", tags=["transactions"], summary= "Get transaction information", description="Item & cost information about transaction", response_model=TransactionOut)
async def get_transaction(id:str):
    fake_database = get_database_information(fake_database_path=fake_database_path)

    if fake_database.get(id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not Found")
    else:
        return TransactionOut(**fake_database.get(id))
    
@router.post("/transactions/create", tags=["transactions"],summary="Create transaction record", description="Create record after user/product availability validation. Return cost record", response_model=TransactionOut)
async def create_transaction(data:TransactionIn):

    # Step 1: Validate the user 
    #TODO: Consolidate shared business logic between user get and transaction route
    fake_database_users = get_database_information(fake_database_path=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'fake_database_users.json')))

    email = data.email.lower()
    if fake_database_users.get(email) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found. Please create user using `/user/create-user`")
    
    # Step 2: Validate product inventory
    #TODO: Validation of business logic should be shared
    fake_database_products = get_database_information(fake_database_path= os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'fake_database_products.json')))

    if fake_database_products.get(data.product_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found. Please create with `products/create`")
    
    elif fake_database_products.get(data.product_id).get("quantity_in_stock") < data.quantity:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=f"Not enough inventory to process transaction. Current Inventory: {fake_database_products.get(data.product_id).get("quantity_in_stock")}")
    
    # Step 3: Decrease product inventory
    #TODO: Decrease of product inventory should be a shared function
    stock = fake_database_products[data.product_id].get("quantity_in_stock")
    stock -= data.quantity
    fake_database_products[data.product_id]["quantity_in_stock"] = stock

    write_database_information(database_information=fake_database_products, fake_database_path= os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'fake_database_products.json')))

    # Step 4: Build the return object 

    product_name = fake_database_products[data.product_id].get("display_name")
    unit_price = fake_database_products[data.product_id].get("unit_price")


    return TransactionOut(
        quantity=data.quantity,
        product_name=product_name,
        price=unit_price*data.quantity/100,
        transaction_id=str(uuid.uuid4())
    )