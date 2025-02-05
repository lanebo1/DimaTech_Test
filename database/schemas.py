from pydantic import BaseModel, EmailStr
from typing import List, Optional
from uuid import UUID, uuid4


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    id: UUID = uuid4()
    email: EmailStr
    full_name: str
    is_admin: bool = False


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    is_admin: bool = False


class Account(BaseModel):
    id: UUID = uuid4()
    user_id: UUID
    balance: float = 0.0


class Payment(BaseModel):
    id: UUID = uuid4()
    account_id: UUID
    amount: float
