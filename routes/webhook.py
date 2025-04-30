from random import randint
from sqlalchemy import cast
from fastapi import HTTPException
from sqlalchemy.future import select
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
import hashlib
import os
from database.schemas import Transaction as TransactionSchema
from auth.auth_ops import verify_signature
from database.database import get_db
from database.models import User, Account, Transaction
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import cast, String

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY")


@router.post("/webhook")
def process_webhook(payload: TransactionSchema, db: AsyncSession = Depends(get_db)):
    if not verify_signature(payload):
        raise HTTPException(status_code=400, detail="Invalid signature")

    query = select(User).where(User.id == payload.user_id)
    result = db.execute(query)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    query = select(Account).where(Account.id == payload.account_id, Account.user_id == payload.user_id)
    result = db.execute(query)
    account = result.scalars().first()
    if not account:
        account = Account(id=payload.account_id, user_id=payload.user_id, balance=0.0)
        db.add(account)
        db.commit()
        db.refresh(account)

    query = select(Transaction).where(Transaction.transaction_id == cast(payload.transaction_id, String))
    result = db.execute(query)
    transaction = result.scalars().first()
    if transaction:
        raise HTTPException(status_code=400, detail="Transaction already processed")

    transaction = Transaction(
        transaction_id=payload.transaction_id,
        account_id=payload.account_id,
        user_id=payload.user_id,
        amount=payload.amount,
        signature=payload.signature
    )
    db.add(transaction)
    account.balance += payload.amount
    db.commit()
    db.refresh(account)

    return {"detail": "Transaction processed successfully"}


def generate_signature(payload: dict) -> str:
    data_string = f"{payload['account_id']}{payload['amount']}{payload['transaction_id']}{payload['user_id']}{SECRET_KEY}"
    return hashlib.sha256(data_string.encode()).hexdigest()


@router.get("/generate-webhook", response_model=TransactionSchema)
def generate_webhook(user_id: str, user_account_id: str = None, db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.id == user_id)
    result = db.execute(query)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_account_id:
        query = select(Account).where(Account.id == user_account_id, Account.user_id == user_id)
        result = db.execute(query)
        account = result.scalars().first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
    else:
        account_id = str(uuid4())
        account = Account(id=account_id, user_id=user_id, balance=0.0)
        db.add(account)
        db.commit()
        db.refresh(account)
        account_created = True

    amount = randint(1, 1000)
    payload = {
        "transaction_id": str(uuid4()),
        "user_id": user_id,
        "account_id": account.id,
        "amount": amount
    }
    payload["signature"] = generate_signature(payload)

    response = payload
    if not user_account_id:
        response["detail"] = "New account created"

    return response
