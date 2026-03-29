from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserProfileInputSchema(BaseModel):
    username: str
    first_name: str
    phone_number: str
    role: str
class UserLoginSchema(BaseModel):
    username: str
    password: str
class UserProfileOutSchema(BaseModel):
    id: int
    username: str
    first_name: str
    phone_number: str
    role: str


class RegionInputSchema(BaseModel):
    name: str

class RegionOutSchema(BaseModel):
    id: int
    name: str

class CityInputSchema(BaseModel):
    name: str
    region_id: int

class CityOutSchema(BaseModel):
    id: int
    name: str
    region_id: int

class DistrictInputSchema(BaseModel):
    name: str
    city_id: int

class DistrictOutSchema(BaseModel):
    id: int
    name: str
    city_id: int

class PropertyImageInputSchema(BaseModel):
    property_id: int
    image: str

class PropertyImageOutSchema(BaseModel):
    id: int
    property_id: int
    image: str

class PropertyDocumentInputSchema(BaseModel):
    property_id: int
    file: str

class PropertyDocumentOutSchema(BaseModel):
    id: int
    property_id: int
    file: str

class PropertyInputSchema(BaseModel):
    title: str
    description: str
    property_type: str
    region_id: int
    city_id: int
    district_id: Optional[int] = None
    address: str
    area: float
    price: float
    rooms: int
    floor: int
    total_floors: int
    seller_id: int

class PropertyOutSchema(PropertyInputSchema):
    id: int
    created_at: datetime
    images: List[PropertyImageOutSchema] = []
    documents: List[PropertyDocumentOutSchema] = []

class ReviewInputSchema(BaseModel):
    author_id: int
    seller_id: int
    rating: int
    comment: str

class ReviewOutSchema(ReviewInputSchema):
    id: int
    created_at: datetime
