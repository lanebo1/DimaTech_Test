from datetime import datetime, timedelta
from fastapi import HTTPException
import jwt
from jwt import ExpiredSignatureError, PyJWTError
from passlib.context import CryptContext
import hashlib
import os

from database.schemas import Transaction

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 300

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def verify_signature(payload: Transaction) -> bool:
    data_string = f"{payload.account_id}{int(payload.amount)}{payload.transaction_id}{payload.user_id}{SECRET_KEY}"
    signature = hashlib.sha256(data_string.encode()).hexdigest()
    print(f"Data String: {data_string}")
    print(f"Generated Signature: {signature}")
    print(f"Provided Signature: {payload.signature}")
    return signature == payload.signature
