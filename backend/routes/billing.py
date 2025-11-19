# backend/routes/billing.py
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from sqlalchemy.orm import Session

from backend.database import get_db, User
from backend.routes.auth import get_current_user  # نستعمل نفس التوكن

PLAN_PRICE_USD = 29
CURRENCY = "USD"
TRIAL_DAYS = 30

router = APIRouter(
    prefix="/billing",
    tags=["billing"],
)


# ================================
#   Schemas
# ================================

class BillingStatus(BaseModel):
    email: str
    is_trial: bool
    trial_ends_at: Optional[datetime] = None
    trial_days_left: int
    is_active: bool
    plan_price: int
    currency: str


class ActivatePayload(BaseModel):
    paypal_subscription_id: str


# ================================
#   Helpers
# ================================

def _compute_status(user: User) -> BillingStatus:
    now = datetime.utcnow()

    is_trial = False
    days_left = 0
    if user.trial_ends_at and user.trial_ends_at > now and not user.is_active:
        is_trial = True
        days_left = (user.trial_ends_at - now).days

    return BillingStatus(
        email=user.email,
        is_trial=is_trial,
        trial_ends_at=user.trial_ends_at,
        trial_days_left=max(days_left, 0),
        is_active=user.is_active,
        plan_price=PLAN_PRICE_USD,
        currency=CURRENCY,
    )


# ================================
#   Routes
# ================================

@router.get("/status", response_model=BillingStatus)
def get_billing_status(
    current_user: User = Depends(get_current_user),
):
    """
    يرجع حالة الاشتراك للمستخدم الحالي:
    - هل هو في الفترة التجريبية
    - كم يوم متبقي
    - هل الاشتراك مفعل
    """
    return _compute_status(current_user)


@router.post("/activate", response_model=BillingStatus)
def activate_subscription(
    payload: ActivatePayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    يُستدعى بعد نجاح الدفع في بايبال:
    - يفعّل الاشتراك
    - يحفظ paypal_subscription_id للرجوع له عند الحاجة
    """

    if current_user.is_active:
        # لو كان مفعل أصلاً نرجع الحالة فقط
        return _compute_status(current_user)

    current_user.is_active = True
    current_user.paypal_subscription_id = payload.paypal_subscription_id

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return _compute_status(current_user)
