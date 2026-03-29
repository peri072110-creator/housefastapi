from fastapi import FastAPI
import uvicorn


from mysite.api.users import user_router
from mysite.api.regions import region_router
from mysite.api.cities import city_router
from mysite.api.district import district_router
from mysite.api.property import property_router
from mysite.api.property_image import property_image_router
from mysite.api.property_doc import property_doc_router
from mysite.api.reviews import review_router
from mysite.api.auth import auth_router


from mysite.admin.setup import setup_admin



app = FastAPI(title="NAYA_GARA_POPOOOOO")


# ================== ROUTERS ==================
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(region_router, prefix="/regions", tags=["Regions"])
app.include_router(city_router, prefix="/cities", tags=["Cities"])
app.include_router(district_router, prefix="/districts", tags=["Districts"])
app.include_router(property_router, prefix="/properties", tags=["Properties"])
app.include_router(property_image_router, prefix="/property-images", tags=["Property Images"])
app.include_router(property_doc_router, prefix="/property-documents", tags=["Property Documents"])
app.include_router(review_router, prefix="/reviews", tags=["Reviews"])


app.include_router(auth_router, prefix="/auth", tags=["Auth"])



setup_admin(app)



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)