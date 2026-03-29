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


from mysite.database.models import District
from mysite.database.schema import DistrictInputSchema, DistrictOutSchema

district_router = APIRouter(prefix="/districts", tags=["Districts"])

@district_router.post("/", response_model=DistrictOutSchema)
def create_district(data: DistrictInputSchema, db: Session = Depends(get_db)):
    obj = District(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@district_router.get("/", response_model=List[DistrictOutSchema])
def list_districts(db: Session = Depends(get_db)):
    return db.query(District).all()

@district_router.get("/{id}", response_model=DistrictOutSchema)
def get_district(id: int, db: Session = Depends(get_db)):
    obj = db.get(District, id)
    if not obj:
        raise HTTPException(404, "District not found")
    return obj

@district_router.put("/{id}", response_model=DistrictOutSchema)
def update_district(id: int, data: DistrictInputSchema, db: Session = Depends(get_db)):
    obj = db.get(District, id)
    if not obj:
        raise HTTPException(404, "District not found")

    for k, v in data.model_dump().items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)
    return obj

@district_router.delete("/{id}")
def delete_district(id: int, db: Session = Depends(get_db)):
    obj = db.get(District, id)
    if not obj:
        raise HTTPException(404, "District not found")

    db.delete(obj)
    db.commit()
    return {"message": "deleted"}