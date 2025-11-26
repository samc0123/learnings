# All routes related to POS transactions 
from fastapi import APIRouter
import os 

router = APIRouter()

#TODO: Implement Fake database and transactions routes to track POS purchases 
fake_database_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'fake_database_transactions.json'))


