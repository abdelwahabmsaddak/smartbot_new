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

from flask import Blueprint, render_template, request, redirect, session
from database import db

auth_bp = Blueprint('auth_bp', __name__)

# ================================
# 🔐 LOGIN
# ================================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = db.fetch_one("SELECT * FROM users WHERE email=? AND password=?", (email, password))

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect('/dashboard')

        return render_template('login.html', error="البريد أو كلمة المرور غير صحيحة")

    return render_template('login.html')
        # إضافة المستخدم في قاعدة البيانات
        db.execute("""
            INSERT INTO users (username, email, password)
            VALUES (?, ?, ?)
        """, (username, email, password))

        return redirect('/login')

    return render_template('register.html')
    @auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.fetch_one(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # تحقق إذا كان المستخدم موجود
        existing = db.fetch_one("SELECT * FROM users WHERE username=? OR email=?", (username, email))
        if existing:
            return render_template('register.html', error="المستخدم موجود مسبقًا")

        # إضافة المستخدم
        db.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )

        return redirect('/login')

    return render_template('register.html')
        if user:
            session['user_id'] = user['id']
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="معلومات خاطئة")

    return render_template('login.html نعم)
