# backend/routes/payments.py
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.database import get_db, User

# ❗ غيّر هذا import حسب ما سميناه في auth route
from backend.routes.auth import get_current_user  # get_current_user يرجع User

router = APIRouter(
    prefix="/api/billing",
    tags=["billing"],
)

TRIAL_DAYS = 30
PLAN_PRICE = 29.0  # دولار
PLAN_NAME = "الخطة الشاملة"


class PaymentConfirm(BaseModel):
    provider: str = "paypal"
    transaction_id: str


@router.get("/status")
def billing_status(
    current_user: User = Depends(get_current_user),
):
    """
    يرجع حالة الباقة للمستخدم الحالي:
    - هل هو في التجربة المجانية؟
    - هل الاشتراك المدفوع شغال؟
    - متى التجديد؟
    """
    status_text = current_user.subscription_status()

    return {
        "plan": PLAN_NAME,
        "price": PLAN_PRICE,
        "trial_ends_at": current_user.trial_ends_at,
        "is_subscriber": current_user.is_subscriber,
        "next_billing_at": current_user.next_billing_at,
        "status_text": status_text,
    }


@router.post("/start-trial")
def start_trial(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    يستعمل فقط إذا حبيت تعيد التجربة (للاختبار).
    في الاستخدام الحقيقي، التجربة تتعمل تلقائيًا وقت التسجيل
    لأننا حطينا default في model.
    """
    now = datetime.now(timezone.utc)
    current_user.trial_ends_at = now + timedelta(days=TRIAL_DAYS)
    current_user.is_subscriber = False
    current_user.next_billing_at = None

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return {
        "message": "تم بدء التجربة المجانية لشهر كامل",
        "trial_ends_at": current_user.trial_ends_at,
    }


@router.post("/confirm-payment")
def confirm_payment(
    data: PaymentConfirm,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    هذه الراوت تُستدعى بعد ما يتم الدفع بنجاح بواسطة بايبال.
    من جهة الفرونت أو Webhook:
    - تتحقق من الدفع عند بايبال
    - ثم تنادي هذا الـ endpoint وتبعث transaction_id

    هنا نحن فقط نعتبر أن الدفع ناجح، ونحدّث الاشتراك.
    """

    if data.provider.lower() != "paypal":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="مزود دفع غير مدعوم حالياً (ندعم PayPal فقط).",
        )

    now = datetime.now(timezone.utc)

    # لو كان لأول مرة يدفع بعد التجربة
    current_user.is_subscriber = True
    current_user.next_billing_at = now + timedelta(days=30)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return {
        "message": "تم تفعيل الاشتراك الشهري بنجاح",
        "plan": PLAN_NAME,
        "price": PLAN_PRICE,
        "next_billing_at": current_user.next_billing_at,
        "transaction_id": data.transaction_id,
    }
