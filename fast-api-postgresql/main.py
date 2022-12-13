from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import List
from database import SessionLocal
import models


app = FastAPI()

db = SessionLocal()

class Item(BaseModel): #serilizer
    id:int
    name:str
    description:str
    price:int
    on_offer:bool

    class Config:
        orm_mode = True

@app.get('/items',response_model=List[Item],status_code=200)
def get_all_items():
    items = db.query(models.Item).all()

    return items

@app.get('/item/{item_id}',response_model=Item,status_code=status.HTTP_200_OK)
def get_an_item(item_id:int):

    item = db.query(models.Item).filter(models.Item.id==item_id).first()
    if item is None:
        raise HTTPException(status_code=400,detail="Item does not exist")
    return item

@app.post('/items',response_model=Item,
        status_code=status.HTTP_201_CREATED)
def create_an_item(item:Item):

    db_item = db.query(models.Item).filter(models.Item.name == item.name).first()

    if db_item is not None:
        raise HTTPException(status_code=400,detail="Item Already Exist")

    new_item = models.Item(
        id = item.id,
        name = item.name,
        price = item.price,
        description = item.description,
        on_offer = item.on_offer
    )
    
    db.add(new_item)
    db.commit()

    return new_item

@app.put('/item/{item_id}',response_model=Item,status_code=status.HTTP_200_OK)
def update_an_item(item_id:int,item:Item):
    item_to_update=db.query(models.Item).filter(models.Item.id==item_id).first()

    item_to_update.name = item.name
    item_to_update.price = item.price
    item_to_update.description = item.description
    item_to_update.on_offer = item.on_offer
    
    db.commit()

    return item


@app.delete('/item/{item_id}')
def delete_an_item(item_id:int):
    item_to_delete = db.query(models.Item).filter(models.Item.id==item_id).first()

    if item_to_delete is None:
        raise HTTPException(status_code=400,
        detail="Item to be deleted does not exist")

    db.delete(item_to_delete)

    return {"message":f"Item with ID={item_to_delete.id} has been deleted"}