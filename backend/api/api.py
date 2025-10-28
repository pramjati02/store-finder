from sqlalchemy.orm import Session
from models import models 
from schemas import schemas

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