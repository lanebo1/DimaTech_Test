from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.crud import get_current_user, is_non_admin_user
from database.models import User, Account, Payment
from database.database import get_db
from database.schemas import User as UserSchema, Account as AccountSchema, Payment as PaymentSchema
from typing import List

router = APIRouter()


@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(is_non_admin_user)):
    return current_user


@router.get("/accounts", response_model=List[AccountSchema])
async def get_accounts(current_user: User = Depends(is_non_admin_user), db: AsyncSession = Depends(get_db)):
    query = select(Account).where(Account.user_id == current_user.id)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/payments", response_model=List[PaymentSchema])
async def get_payments(current_user: User = Depends(is_non_admin_user), db: AsyncSession = Depends(get_db)):
    query = select(Payment).join(Account).where(Account.user_id == current_user.id)
    result = await db.execute(query)
    return result.scalars().all()
