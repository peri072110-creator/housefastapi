from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from mysite.database.models import City
from mysite.database.schema import CityInputSchema, CityOutSchema
from mysite.database.db import SessionLocal

city_router = APIRouter(prefix="/cities")

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@city_router.post("/", response_model=CityOutSchema)
async def create_city(city: CityInputSchema, db: Session = Depends(get_db)):
    city_db = City(**city.dict())
    db.add(city_db)
    db.commit()
    db.refresh(city_db)
    return city_db


@city_router.get("/", response_model=List[CityOutSchema])
async def list_cities(db: Session = Depends(get_db)):
    return db.query(City).all()


@city_router.get("/{city_id}", response_model=CityOutSchema)
async def get_city(city_id: int, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(status_code=404, detail="City not found")
    return city_db


@city_router.put("/{city_id}", response_model=CityOutSchema)
async def update_city(city_id: int, city: CityInputSchema, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(status_code=404, detail="City not found")

    for key, value in city.dict().items():
        setattr(city_db, key, value)

    db.commit()
    db.refresh(city_db)
    return city_db


@city_router.delete("/{city_id}")
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(status_code=404, detail="City not found")

    db.delete(city_db)
    db.commit()
    return {"message": "City deleted successfully"}