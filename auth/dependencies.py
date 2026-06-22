from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from dependencies import get_db
from models import User
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def decode_token(token: str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload

    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid token")


def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    payload = decode_token(token)
    user_uuid = payload.get("sub")
    if not user_uuid:
        raise HTTPException(status_code=401,detail="Invalid token")

    user = (db.query(User).filter(User.user_uuid == user_uuid).first())
    if not user:
        raise HTTPException(status_code=401,detail="User not found")
    return user