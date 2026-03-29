# mysite/admin/setup.py
from fastapi import FastAPI
from sqladmin import Admin, ModelView
from mysite.database.db import engine
from mysite.database.models import (
    UserProfile, Region, City, District, Property,
    PropertyImage, PropertyDocument, Review
)

def setup_admin(app: FastAPI):
    admin = Admin(app, engine=engine, title="HOUSE-ADMIN")  # <- убрали template_mode

    class UserProfileAdmin(ModelView, model=UserProfile):
        column_list = [UserProfile.id, UserProfile.username, UserProfile.first_name, UserProfile.role]

    class RegionAdmin(ModelView, model=Region):
        column_list = [Region.id, Region.name]

    class CityAdmin(ModelView, model=City):
        column_list = [City.id, City.name, City.region_id]

    class DistrictAdmin(ModelView, model=District):
        column_list = [District.id, District.name, District.city_id]

    class PropertyAdmin(ModelView, model=Property):
        column_list = [Property.id, Property.title, Property.property_type, Property.price, Property.seller_id]

    class PropertyImageAdmin(ModelView, model=PropertyImage):
        column_list = [PropertyImage.id, PropertyImage.property_id, PropertyImage.image]

    class PropertyDocumentAdmin(ModelView, model=PropertyDocument):
        column_list = [PropertyDocument.id, PropertyDocument.property_id, PropertyDocument.file]

    class ReviewAdmin(ModelView, model=Review):
        column_list = [Review.id, Review.author_id, Review.seller_id, Review.rating]

    # Регистрируем все модели
    admin.add_view(UserProfileAdmin)
    admin.add_view(RegionAdmin)
    admin.add_view(CityAdmin)
    admin.add_view(DistrictAdmin)
    admin.add_view(PropertyAdmin)
    admin.add_view(PropertyImageAdmin)
    admin.add_view(PropertyDocumentAdmin)
    admin.add_view(ReviewAdmin)