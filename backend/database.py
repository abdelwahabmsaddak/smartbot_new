# backend/database.py
from datetime import datetime, timedelta, timezone

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./smartbot.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # 🟡 الباقة الوحيدة: شهر مجاني ثم 29$
    # تاريخ نهاية التجربة المجانية
    trial_ends_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc) + timedelta(days=30),
    )

    # هل عنده اشتراك مدفوع نشط؟
    is_subscriber = Column(Boolean, default=False)

    # متى سيتم تجديد الاشتراك الشهري القادم؟
    next_billing_at = Column(DateTime, nullable=True)

    def subscription_status(self):
        """يرجع حالة الاشتراك كنص بسيط"""
        now = datetime.now(timezone.utc)

        # إذا عنده اشتراك مدفوع ومزال وقت على الفاتورة الجاية
        if self.is_subscriber and self.next_billing_at and self.next_billing_at > now:
            days_left = (self.next_billing_at - now).days
            return f"اشتراك مدفوع، يتجدد بعد {days_left} يوم"

        # لو ما دفعش بعد، لكن التجربة مازالت جارية
        if self.trial_ends_at and self.trial_ends_at > now:
            days_left = (self.trial_ends_at - now).days
            return f"تجربة مجانية، متبقي {days_left} يوم"

        # انتهت التجربة وما ثماش اشتراك
        return "منتهي، يلزم تجدد الاشتراك"


def get_db():
    """Dependency تستعملها في الراوترات"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
