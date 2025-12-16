from flask import Blueprint, render_template

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    # user وهمي (تو)
    user = {
        "username": "Abdelwahab"
    }

    dashboard_data = {
        "balance": "1250 USDT",
        "open_trades": 2,
        "status": "AI Running",
        "daily_profit": "+3.4%"
    }

    return render_template(
        "dashboard.html",
        user=user,
        data=dashboard_data
    )
