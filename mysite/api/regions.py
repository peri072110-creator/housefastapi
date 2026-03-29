from sqlalchemy.orm import Session
from mysite.database.db import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from mysite.database.models import Region
from mysite.database.schema import RegionInputSchema, RegionOutSchema

region_router = APIRouter(prefix="/regions", tags=["Regions"])

@region_router.post("/", response_model=RegionOutSchema)
def create_region(data: RegionInputSchema, db: Session = Depends(get_db)):
    obj = Region(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@region_router.get("/", response_model=List[RegionOutSchema])
def list_regions(db: Session = Depends(get_db)):
    return db.query(Region).all()

@region_router.get("/{id}", response_model=RegionOutSchema)
def get_region(id: int, db: Session = Depends(get_db)):
    obj = db.get(Region, id)
    if not obj:
        raise HTTPException(404, "Region not found")
    return obj

@region_router.put("/{id}", response_model=RegionOutSchema)
def update_region(id: int, data: RegionInputSchema, db: Session = Depends(get_db)):
    obj = db.get(Region, id)
    if not obj:
        raise HTTPException(404, "Region not found")

    obj.name = data.name
    db.commit()
    db.refresh(obj)
    return obj

@region_router.delete("/{id}")
def delete_region(id: int, db: Session = Depends(get_db)):
    obj = db.get(Region, id)
    if not obj:
        raise HTTPException(404, "Region not found")

    db.delete(obj)
    db.commit()
    return {"message": "deleted"}