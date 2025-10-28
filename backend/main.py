from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import models
from schemas import schemas
from api import api
from database import database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

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

