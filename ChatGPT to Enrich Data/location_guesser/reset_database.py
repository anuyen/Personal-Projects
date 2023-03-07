"""
This script is used to reset the database

The main script returns "Not in given list" when the name is not in the given list

In order to increase adaptability --> the script will remove any key:value with the 
value "Not in given list"
"""

import json

def clean(value: str)-> str:
    if "Not in given list" in value:
        return value.split('\n')[0]
    else:
        return value


def reset_location_database(file_location: str, backup_location: str)-> None:
    """
    Backup data before cleaning
    """
    data_dict: dict = {}

    # Intake data
    with open(file_location,'r') as file:
        data_dict = json.load(file)
    with open(backup_location,'w') as file:
        json.dump(data_dict,file)

    data_dict = {key:value for key,value in data_dict.items() if value!="Not in given list"}

    data_dict = {key:value for key,value in data_dict.items() if value is not None}

    data_dict = {key:clean(value) for key,value in data_dict.items()}

    with open(file_location,'w') as file:
        json.dump(data_dict,file)