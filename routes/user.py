from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.crud import get_current_user
from database.models import User, Account, Payment
from database.database import get_db
from database.schemas import User as UserSchema, Account as AccountSchema, Payment as PaymentSchema, Token
from pydantic import BaseModel
from typing import List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.email == form_data.username)
    result = await db.execute(query)
    user = result.scalars().first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": user.email, "token_type": "bearer"}

#TODO: fix user auth
@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/accounts", response_model=List[AccountSchema])
async def get_accounts(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    query = select(Account).where(Account.user_id == current_user.id)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/payments", response_model=List[PaymentSchema])
async def get_payments(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    query = select(Payment).join(Account).where(Account.user_id == current_user.id)
    result = await db.execute(query)
    return result.scalars().all()
