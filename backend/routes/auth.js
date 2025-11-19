from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, constr
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext

# 🔹 استيراد الداتا بيز والموديل User من database.py
from backend.database import get_db, User  # عدّل المسار لو ملفك مختلف

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

# ==========================
# إعدادات الأمان و الـ JWT
# ==========================

SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_ME"  # غيّرها في المشروع الحقيقي
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # توكن صالح لأسبوع

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ==========================
#   مخططات (Schemas)
# ==========================

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    trial_ends_at: Optional[datetime]

    class Config:
        from_attributes = True  # لـ SQLAlchemy


# ==========================
#   دوال مساعدة
# ==========================

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="بيانات الدخول غير صالحة",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise credentials_exception

    return user


# ==========================
#     الراوتات الفعلية
# ==========================

@router.post("/register", response_model=Token, status_code=201)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    تسجيل مستخدم جديد:
    - إيميل + باسورد
    - شهر مجاني تجريبي تلقائي
    - يرجّع JWT توكن
    """

    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="هذا البريد مسجّل من قبل",
        )

    hashed = get_password_hash(user_in.password)

    # شهر مجاني
    trial_ends_at = datetime.utcnow() + timedelta(days=30)

    user = User(
        email=user_in.email,
        hashed_password=hashed,
        is_active=True,
        trial_ends_at=trial_ends_at,
        plan="trial",          # لو عندك حقل plan في الموديل
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token({"sub": user.id})
    return Token(access_token=access_token)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    تسجيل دخول:
    يستقبل email في حقل username (هكذا يعمل OAuth2PasswordRequestForm)
    + password
    """
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="الإيميل أو كلمة السر غير صحيحة",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="الحساب غير مُفعّل",
        )

    access_token = create_access_token({"sub": user.id})
    return Token(access_token=access_token)


@router.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    """
    يرجّع بيانات المستخدم الحالي:
    - id
    - email
    - هل الحساب مفعل
    - نهاية الفترة التجريبية
    """
    return current_user
