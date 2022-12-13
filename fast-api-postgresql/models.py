from database import Base
from sqlalchemy import String, Boolean, Integer, Column, Text

class Item(Base):
    __tablename__='items'
    price=Column(Integer,nullable=False)
    id=Column(Integer,primary_key=True)
    name=Column(String(255),nullable=False,unique=True)
    description=Column(Text,nullable=False)
    on_offer=Column(Boolean,default=False)

    def __repr__(self):
        return f"<Item name={self.name} price={self.price}>"