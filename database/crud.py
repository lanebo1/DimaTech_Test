import os

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from database.models import User, Account, Payment

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    query = select(User).where(User.email == decoded_token['sub'])
    result = await db.execute(query)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user


async def is_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")
    return current_user


async def is_non_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access forbidden: Non-admins only")
    return current_user
