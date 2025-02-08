from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models import User, Account, pwd_context
from database.database import get_db
from database.schemas import User as UserSchema, Account as AccountSchema, UserCreate
from database.crud import is_admin_user
from typing import List

router = APIRouter()


@router.post("/users", response_model=UserSchema)
def create_user(user: UserCreate, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(is_admin_user)):
    db_user = User(**user.dict())
    if db_user.email in [u.email for u in get_users(db)]:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user.password = pwd_context.hash(db_user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}")
def delete_user(user_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(is_admin_user)):
    query = select(User).where(User.id == user_id)
    result = db.execute(query)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}


@router.put("/users/{user_id}", response_model=UserSchema)
def update_user(user_id: str, user: UserSchema, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(is_admin_user)):
    query = select(User).where(User.id == user_id)
    result = db.execute(query)
    db_user = result.scalars().first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/users", response_model=List[UserSchema])
def get_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(is_admin_user)):
    query = select(User)
    result = db.execute(query)
    return result.scalars().all()


@router.get("/users/{user_id}/accounts", response_model=List[AccountSchema])
def get_user_accounts(user_id: str, db: AsyncSession = Depends(get_db),
                            current_user: User = Depends(is_admin_user)):
    query = select(Account).where(Account.user_id == user_id)
    result = db.execute(query)
    return result.scalars().all()
