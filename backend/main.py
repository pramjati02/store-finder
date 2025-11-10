from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models import models
from schemas import schemas
from api import api
from database import database
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Dependency: get a fresh DB session per request
def get_db():
    db = database.session_local()
    try:
        yield db
    finally:
        db.close()

@app.get("/stores/", response_model=list[schemas.StoreRead])
def read_stores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return api.get_stores(db, skip=skip, limit=limit)

@app.post("/stores/", response_model=schemas.StoreRead)
def create_store(store: schemas.StoreCreate, db: Session = Depends(get_db)):
    return api.create_store(db, store)

@app.get("/stores/nearby", response_model = list[schemas.StoreRead])
def find_nearby_stores(
    address: str = Query(..., description = "User inputted address or postcode"),
    radius_km: float = 2,
    db: Session = Depends(get_db)
):
    # Convert address to coordinates
    coords = api.geocode_address(address)
    if not coords:
        raise HTTPException(status_code=404, detail="Address not found")
    
    user_lat, user_lon = coords # user inputted address convert to coordinates

    # Query all stores 
    stores = api.get_stores(db, skip=0, limit=10000)

    # Compute distance for each store
    nearby_stores = []

    for s in stores:
        distance = api.haversine(user_lat, user_lon, s.latitude, s.longitude)
        if distance <= radius_km: # checking if distance is smaller or equal to the minimum radius set out
            nearby_stores.append((s, distance))

    # sort by distance
    nearby_stores.sort(key=lambda x:x[1])

    # Return top 10 closest
    return [s for s, _ in nearby_stores[:20]]




