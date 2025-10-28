from pydantic import BaseModel 

# Define the base model format which is communicated via the API
class StoreBase(BaseModel): 
    name: str
    type: str
    region: str
    latitude: float
    longitude: float
    address: str

# Creating a store using the base model
class StoreCreate(StoreBase):
    pass

class StoreRead(StoreBase):
    id: int

    class Config:
        orm_mode = True
