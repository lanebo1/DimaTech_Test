from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from auth.auth_routes import create_access_token
from database.models import User, pwd_context
from database.database import get_db
from database.schemas import Token, UserCreate
from fastapi.security import OAuth2PasswordRequestForm

from routes.admin import get_users

router = APIRouter()


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/users")
def read_users(db: AsyncSession = Depends(get_db)):
    query = select(User)
    result = db.execute(query)
    return result.scalars().all()


@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.email == form_data.username)
    result = db.execute(query)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/create_user", response_model=UserCreate)
def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = User(**user.dict())
    if db_user.email in [u.email for u in get_users(db)]:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user.password = pwd_context.hash(db_user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user