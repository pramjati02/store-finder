from sqlalchemy.orm import Session
from models import models 
from schemas import schemas
import math
import requests

# db: Session = session that is required to communicate with the database 

# Creating a store, includies schema StoreCreate that allows the creation of a store in the db
def create_store(db: Session, store: schemas.StoreCreate): 
    db_store = models.Store(**store.dict()) # stores the dictionary of the created schema into the model (** = unpacks dictionary)
    db.add(db_store) # adds our model to the db
    db.commit() # commit  the changes to the db
    db.refresh(db_store) # gets the latest version of what you have just stored, just as a check
    return db_store 

def get_stores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Store).offset(skip).limit(limit).all()

# Convert address to coordinates using OpenStreetMap (Nominatim), retrieving longitude and latitude
def geocode_address(address: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }

    response = requests.get(url, params=params, headers={"User-Agent": "store-finder"})
    data = response.json()
    if not data:
        return None
    lat = float(data[0]["lat"])
    lon =  float(data[0]["lon"])
    return lat, lon 

# calculate distance between two longitude and latitude points (Haversine)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371 # Earth radius in kilometers 
    
    # calculate difference between longitudes and latitudes
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # distance in km
