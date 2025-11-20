from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt

from backend.database import get_db
from backend.database import User  # الموديل متاع اليوزر

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_ME"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ----------------------------------------------------------
#  helper functions
# ----------------------------------------------------------

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_token(data: dict, expires_minutes=60*24*30):  # شهر
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ----------------------------------------------------------
#  Register Route
# ----------------------------------------------------------

@router.post("/register")
def register(email: str, password: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(status_code=400, detail="الحساب موجود مسبقاً")

    new_user = User(
        email=email,
        password=hash_password(password),
        is_active=True,
        trial_ends_at=datetime.utcnow() + timedelta(days=30)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_token({"user_id": new_user.id})

    return {"message": "تم إنشاء الحساب", "token": token}


# ----------------------------------------------------------
#  Login Route
# ----------------------------------------------------------

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="الحساب غير موجود")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="كلمة السر خاطئة")

    token = create_token({"user_id": user.id})

    return {"message": "تسجيل دخول ناجح", "token": token}
