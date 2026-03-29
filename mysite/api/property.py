from sqlalchemy.orm import Session
from mysite.database.db import SessionLocal
from fastapi import APIRouter, HTTPException, Depends
from typing import List
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from mysite.database.models import Property
from mysite.database.schema import PropertyInputSchema, PropertyOutSchema

property_router = APIRouter(prefix="/properties" )

@property_router.post("/", response_model=PropertyOutSchema)
def create_property(data: PropertyInputSchema, db: Session = Depends(get_db)):
    obj = Property(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@property_router.get("/", response_model=List[PropertyOutSchema])
def list_properties(db: Session = Depends(get_db)):
    return db.query(Property).all()

@property_router.get("/{id}", response_model=PropertyOutSchema)
def get_property(id: int, db: Session = Depends(get_db)):
    obj = db.get(Property, id)
    if not obj:
        raise HTTPException(404, "Property not found")
    return obj

@property_router.put("/{id}", response_model=PropertyOutSchema)
def update_property(id: int, data: PropertyInputSchema, db: Session = Depends(get_db)):
    obj = db.get(Property, id)
    if not obj:
        raise HTTPException(404, "Property not found")

    for k, v in data.model_dump().items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)
    return obj

@property_router.delete("/{id}")
def delete_property(id: int, db: Session = Depends(get_db)):
    obj = db.get(Property, id)
    if not obj:
        raise HTTPException(404, "Property not found")

    db.delete(obj)
    db.commit()
    return {"message": "deleted"}