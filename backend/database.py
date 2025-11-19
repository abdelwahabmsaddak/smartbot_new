from datetime import datetime, timedelta

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

    created_at = Column(DateTime, default=datetime.utcnow)

    # الاشتراك
    trial_end = Column(DateTime, nullable=False)          # نهاية الشهر المجاني
    subscription_status = Column(String, default="trial") # trial, active, canceled, expired
    paypal_subscription_id = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)


def init_db():
    Base.metadata.create_all(bind=engine)
