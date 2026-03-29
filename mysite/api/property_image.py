
from mysite.database.db import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from mysite.database.models import PropertyImage
from mysite.database.schema import PropertyImageInputSchema, PropertyImageOutSchema

property_image_router = APIRouter(prefix="/property-images" )
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@property_image_router.post("/", response_model=PropertyImageOutSchema)
def create_image(data: PropertyImageInputSchema, db: Session = Depends(get_db)):
    obj = PropertyImage(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@property_image_router.get("/", response_model=List[PropertyImageOutSchema])
def list_images(db: Session = Depends(get_db)):
    return db.query(PropertyImage).all()


@property_image_router.get("/{id}", response_model=PropertyImageOutSchema)
def get_image(id: int, db: Session = Depends(get_db)):
    obj = db.get(PropertyImage, id)
    if not obj:
        raise HTTPException(404, "Image not found")
    return obj


@property_image_router.put("/{id}", response_model=PropertyImageOutSchema)
def update_image(id: int, data: PropertyImageInputSchema, db: Session = Depends(get_db)):
    obj = db.get(PropertyImage, id)
    if not obj:
        raise HTTPException(404, "Image not found")

    for k, v in data.model_dump().items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)
    return obj


@property_image_router.delete("/{id}")
def delete_image(id: int, db: Session = Depends(get_db)):
    obj = db.get(PropertyImage, id)
    if not obj:
        raise HTTPException(404, "Image not found")

    db.delete(obj)
    db.commit()
    return {"message": "deleted"}