from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated, List
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
from flask_sqlalchemy import SQLAlchemy
import models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = {
    "http://localhost:3000",
}

app.add_middleware(
CORSMiddleware,
allow_origins=origins, # Allows all origins
allow_credentials=True,
allow_methods=["*"], # Allows all methods
allow_headers=["*"] # Allows all headers
)

class TransactionBase(BaseModel):
    price: int
    calories: int
    sugar:int
    ingredients:str
    is_list:bool
    recipes:str

class TransactionModel(TransactionBase):
    id: int

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

models.Base.metadata.create_all(bind=engine)

@app.post("/transactions/", response_model=TransactionModel)
async def create_transaction(grocery_items: TransactionBase, db: db_dependency):
    db_grocery_items = models.Transaction(**grocery_items.dict())
    db.add(db_grocery_items)
    db.commit()
    db.refresh(db_grocery_items)
    return db_grocery_items

@app.get("/transactions/", response_model=List[TransactionModel])
async def read_transactions(db: db_dependency, skip: int=0, limit:int=100):
    grocery_items = db.query(models.Transaction).offset(skip).limit(limit).all()
    return grocery_items