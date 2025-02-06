from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from auth.auth_routes import create_access_token
from database.models import User
from database.database import get_db
from database.schemas import Token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.email == form_data.username)
    result = await db.execute(query)
    user = result.scalars().first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
