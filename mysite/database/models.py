from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime, Float, Enum
from datetime import datetime
from typing import Optional, List
class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=False)
    user_id: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class UserProfile(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    first_name: Mapped[str] = mapped_column(String(30))
    phone_number: Mapped[str] = mapped_column(String, unique=True)

    role: Mapped[str] = mapped_column(
        Enum('admin', 'seller', 'buyer', name='role_enum')
    )

    properties: Mapped[List["Property"]] = relationship(back_populates="seller")
    reviews_written: Mapped[List["Review"]] = relationship(
        back_populates="author",
        foreign_keys="Review.author_id"
    )
    reviews_received: Mapped[List["Review"]] = relationship(
        back_populates="seller",
        foreign_keys="Review.seller_id"
    )

class Region(Base):
    __tablename__ = 'regions'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

    cities: Mapped[List["City"]] = relationship(back_populates="region")
    properties: Mapped[List["Property"]] = relationship(back_populates="region")


class City(Base):
    __tablename__ = 'cities'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"))
    region: Mapped["Region"] = relationship(back_populates="cities")
    districts: Mapped[List["District"]] = relationship(back_populates="city")
    properties: Mapped[List["Property"]] = relationship(back_populates="city")


class District(Base):
    __tablename__ = 'districts'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    city: Mapped["City"] = relationship(back_populates="districts")
    properties: Mapped[List["Property"]] = relationship(back_populates="district")

class Property(Base):
    __tablename__ = 'properties'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    property_type: Mapped[str] = mapped_column(
        Enum('apartment', 'house', 'land', 'commercial', 'studio', name='property_type_enum')
    )
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"))
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    district_id: Mapped[int] = mapped_column(ForeignKey("districts.id"), nullable=True)
    region: Mapped["Region"] = relationship(back_populates="properties")
    city: Mapped["City"] = relationship(back_populates="properties")
    district: Mapped["District"] = relationship(back_populates="properties")
    address: Mapped[str] = mapped_column(String)

    area: Mapped[float] = mapped_column(Float)
    price: Mapped[float] = mapped_column(Float)

    rooms: Mapped[int] = mapped_column(Integer)
    floor: Mapped[int] = mapped_column(Integer)
    total_floors: Mapped[int] = mapped_column(Integer)

    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    seller: Mapped["UserProfile"] = relationship(back_populates="properties")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    images: Mapped[List["PropertyImage"]] = relationship(back_populates="property")
    documents: Mapped[List["PropertyDocument"]] = relationship(back_populates="property")


class PropertyImage(Base):
    __tablename__ = 'property_images'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
    property: Mapped["Property"] = relationship(back_populates="images")
    image: Mapped[str] = mapped_column(String)


class PropertyDocument(Base):
    __tablename__ = 'property_documents'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
    property: Mapped["Property"] = relationship(back_populates="documents")
    file: Mapped[str] = mapped_column(String)


class Review(Base):
    __tablename__ = 'reviews'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["UserProfile"] = relationship(
        back_populates="reviews_written",
        foreign_keys=[author_id]
    )
    seller: Mapped["UserProfile"] = relationship(
        back_populates="reviews_received",
        foreign_keys=[seller_id]
    )
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)