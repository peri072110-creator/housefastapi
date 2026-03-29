from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional

from mysite.database.db import SessionLocal
from mysite.database.models import UserProfile, RefreshToken
from mysite.database.schema import UserProfileInputSchema, UserLoginSchema




SECRET_KEY = "super_secret_key"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


auth_router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False




def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    return create_access_token(
        data,
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )




@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserProfileInputSchema, db: Session = Depends(get_db)):

    if db.query(UserProfile).filter(UserProfile.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    if db.query(UserProfile).filter(UserProfile.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        age=user.age,
        avatar=user.avatar,
        phone_number=user.phone_number,
        password=get_password_hash(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}




@auth_router.post("/login")
async def login(user: UserLoginSchema, db: Session = Depends(get_db)):

    user_db = db.query(UserProfile).filter(
        UserProfile.username == user.username
    ).first()

    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, user_db.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    access_token = create_access_token({"sub": str(user_db.id)})
    refresh_token = create_refresh_token({"sub": str(user_db.id)})

    db_refresh = RefreshToken(
        token=refresh_token,
        user_id=user_db.id
    )

    db.add(db_refresh)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }




@auth_router.post("/refresh")
async def refresh(refresh_token: str, db: Session = Depends(get_db)):

    stored_token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token
    ).first()

    if not stored_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        new_access_token = create_access_token({"sub": str(user_id)})

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")




@auth_router.post("/logout")
async def logout(refresh_token: str, db: Session = Depends(get_db)):

    stored_token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token
    ).first()

    if not stored_token:
        raise HTTPException(status_code=404, detail="Token not found")

    db.delete(stored_token)
    db.commit()

    return {"message": "Successfully logged out"}
