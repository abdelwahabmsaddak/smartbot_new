from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, constr
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext

from backend.database import get_db, User

router = APIRouter(prefix="/auth", tags=["auth"])

# ===========================================================
# JWT Settings
# ===========================================================
SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_ME"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24h

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ===========================================================
# Schemas
# ===========================================================
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
        from_attributes = True

# ===========================================================
# Helpers
# ===========================================================
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def hash_password(password: str):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ===========================================================
# Register
# ===========================================================
@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):

    exists = db.query(User).filter(User.email == user.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    trial_end = datetime.utcnow() + timedelta(days=30)

    new_user = User(
        email=user.email,
        password=hash_password(user.password),
        is_active=True,
        trial_ends_at=trial_end
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# ===========================================================
# Login
# ===========================================================
@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}

# ===========================================================
# Get current authenticated user
# ===========================================================
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")
