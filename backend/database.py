from datetime import datetime, timedelta

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# لو حاب Postgres بعد نبدل هذا الرابط فقط
DATABASE_URL = "sqlite:///smartbot.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # ربط مع الاشتراك
    subscription = relationship("Subscription", back_populates="user", uselist=False)

    # إعدادات المخاطر (اختيارية الآن)
    max_risk_per_trade = Column(Float, default=1.0)  # ٪ من الرصيد
    max_daily_loss = Column(Float, default=5.0)      # ٪
    leverage = Column(Float, default=1.0)

    # تليجرام (لاحقاً نستعمله)
    telegram_chat_id = Column(String(64), nullable=True)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # حالة الاشتراك
    is_active = Column(Boolean, default=True)

    # تجربة مجانية
    trial_start = Column(DateTime, default=datetime.utcnow)
    trial_end = Column(DateTime, nullable=False)

    # التجديد الشهري
    next_billing_date = Column(DateTime, nullable=True)
    price_monthly = Column(Float, default=29.0)

    # آخر تحديث
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="subscription")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    type = Column(String(50))  # signal / risk / system ...
    message = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """إنشاء الجداول لو مش موجودة"""
    Base.metadata.create_all(bind=engine)


def create_trial_subscription(user):
    """يُنشئ اشتراك شهر مجاني لمستخدم جديد"""
    db = SessionLocal()
    try:
        trial_days = 30
        now = datetime.utcnow()
        sub = Subscription(
            user_id=user.id,
            is_active=True,
            trial_start=now,
            trial_end=now + timedelta(days=trial_days),
            next_billing_date=now + timedelta(days=trial_days),
        )
        db.add(sub)
        db.commit()
    finally:
        db.close()


def get_db():
    """Dependency بسيطة لاستعمالها في الراوتس"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
