# All routes related to POS transactions 
from fastapi import APIRouter, status, HTTPException
import os, json, uuid
from schemas.transactions import TransactionIn, TransactionOut
from models.database_operations import get_database_information, write_database_information



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
    return data