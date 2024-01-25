from database import Base 
from sqlalchemy import Column, Integer, String, Boolean, Float

class Transaction(Base):
    __tablename__ = 'grocery_items'
    
    id = Column(Integer, primary_key = True, index = True)
    price = Column(Integer)
    calories = Column(Integer)
    sugar = Column(Integer)
    ingredients = Column(String)
    is_list = Column(Boolean)
    recipes = Column(String)