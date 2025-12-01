from typing import Dict
import json

def get_database_information(fake_database_path:str) -> Dict[str, Dict[str,str]]:
    '''
    Retrieve fake database information, helper method 
    '''
    

    fake_database = {}
    try:
        with open(fake_database_path,'r') as f:
            fake_database: dict = json.load(f)
            return fake_database
    except (FileNotFoundError, json.JSONDecodeError):
        print('Database empty, initializing new database')
        return fake_database

def write_database_information(database_information:dict, fake_database_path:str) -> None:
    '''
    Write back to the fake database, helper method
    '''

    with open(fake_database_path,'w') as f:
        json.dump(database_information, f)
    f.close()
