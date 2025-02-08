from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.crud import is_non_admin_user
from database.models import User, Account, Transaction
from database.database import get_db
from database.schemas import User as UserSchema, Account as AccountSchema, Transaction as TransactionSchema
from typing import List

router = APIRouter()


@router.get("/me", response_model=UserSchema)
def read_users_me(current_user: User = Depends(is_non_admin_user)):
    return current_user


@router.get("/accounts", response_model=List[AccountSchema])
def get_accounts(current_user: User = Depends(is_non_admin_user), db: AsyncSession = Depends(get_db)):
    query = select(Account).where(Account.user_id == current_user.id)
    result = db.execute(query)
    return result.scalars().all()


@router.get("/payments", response_model=List[TransactionSchema])
def get_payments(current_user: User = Depends(is_non_admin_user), db: AsyncSession = Depends(get_db)):
    query = select(Transaction).join(Account).where(Account.user_id == current_user.id)
    result = db.execute(query)
    return result.scalars().all()
