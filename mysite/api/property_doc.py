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
from mysite.database.models import PropertyDocument
from mysite.database.schema import PropertyDocumentInputSchema, PropertyDocumentOutSchema

property_doc_router = APIRouter(prefix="/property-doc" )


@property_doc_router.post("/", response_model=PropertyDocumentOutSchema)
def create_doc(data: PropertyDocumentInputSchema, db: Session = Depends(get_db)):
    obj = PropertyDocument(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@property_doc_router.get("/", response_model=List[PropertyDocumentOutSchema])
def list_docs(db: Session = Depends(get_db)):
    return db.query(PropertyDocument).all()


@property_doc_router.get("/{id}", response_model=PropertyDocumentOutSchema)
def get_doc(id: int, db: Session = Depends(get_db)):
    obj = db.get(PropertyDocument, id)
    if not obj:
        raise HTTPException(404, "Document not found")
    return obj


@property_doc_router.put("/{id}", response_model=PropertyDocumentOutSchema)
def update_doc(id: int, data: PropertyDocumentInputSchema, db: Session = Depends(get_db)):
    obj = db.get(PropertyDocument, id)
    if not obj:
        raise HTTPException(404, "Document not found")

    for k, v in data.model_dump().items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)
    return obj


@property_doc_router.delete("/{id}")
def delete_doc(id: int, db: Session = Depends(get_db)):
    obj = db.get(PropertyDocument, id)
    if not obj:
        raise HTTPException(404, "Document not found")

    db.delete(obj)
    db.commit()
    return {"message": "deleted"}