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
from mysite.database.models import Review
from mysite.database.schema import ReviewInputSchema, ReviewOutSchema

review_router = APIRouter(prefix="/reviews", tags=["Reviews"])


@review_router.post("/", response_model=ReviewOutSchema)
def create_review(data: ReviewInputSchema, db: Session = Depends(get_db)):
    obj = Review(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@review_router.get("/", response_model=List[ReviewOutSchema])
def list_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()


@review_router.get("/{id}", response_model=ReviewOutSchema)
def get_review(id: int, db: Session = Depends(get_db)):
    obj = db.get(Review, id)
    if not obj:
        raise HTTPException(404, "Review not found")
    return obj


@review_router.put("/{id}", response_model=ReviewOutSchema)
def update_review(id: int, data: ReviewInputSchema, db: Session = Depends(get_db)):
    obj = db.get(Review, id)
    if not obj:
        raise HTTPException(404, "Review not found")

    for k, v in data.model_dump().items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)
    return obj


@review_router.delete("/{id}")
def delete_review(id: int, db: Session = Depends(get_db)):
    obj = db.get(Review, id)
    if not obj:
        raise HTTPException(404, "Review not found")

    db.delete(obj)
    db.commit()
    return {"message": "deleted"}