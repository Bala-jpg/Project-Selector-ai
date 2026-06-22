from passlib.context import CryptContext
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models import User
from pydantic import BaseModel,EmailStr
from datetime import datetime, timedelta
from jose import jwt
from auth.dependencies import get_current_user
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")



class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_uuid: str
    username: str
    email: EmailStr

    class Config:
        from_attributes = True



pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str,hashed_password: str):
    return pwd_context.verify(plain_password,hashed_password)


def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.now() + timedelta(minutes=30)
    payload.update({"exp": expire})
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

router=APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# to register a user
@router.post("/register",response_model=UserResponse)
def register(user: UserRegister,db: Session = Depends(get_db)):

    email_exists = db.query(User).filter(User.email == user.email).first()

    if email_exists:
        raise HTTPException(status_code=400,detail="Email already exists")

    username_exists = db.query(User).filter(User.username == user.username).first()

    if username_exists:
        raise HTTPException(status_code=400,detail="Username already exists")

    new_user = User(username=user.username,email=user.email,password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


#to login in user
@router.post("/login")
def login(user: UserLogin,db: Session = Depends(get_db)):

    db_user = (db.query(User).filter(User.email == user.email).first())

    if not db_user:
        raise HTTPException(status_code=401,detail="Invalid credentials")

    if not verify_password(user.password,db_user.password):
        raise HTTPException(status_code=401,detail="Invalid credentials")

    token = create_access_token({"sub": db_user.user_uuid})

    return {"access_token": token,"token_type": "bearer",
                "user": {
        "user_uuid": db_user.user_uuid,
        "username": db_user.username,
        "email": db_user.email
    }
}
    

# idk
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "user_uuid": current_user.user_uuid,
        "username": current_user.username,
        "email": current_user.email
    }