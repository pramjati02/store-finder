from sqlalchemy import Column, Integer, String, Float
from database.database import Base

# Initializing a table named 'stores' in the db, inheriting from Base
class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String, index=True)
    region = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String)


