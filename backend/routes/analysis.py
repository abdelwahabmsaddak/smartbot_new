from flask import Blueprint, request, session, jsonify, render_template
import sqlite3
import openai
from flask import Blueprint, request, jsonify
import yfinance as yf
import pandas as pd

analysis_bp = Blueprint('analysis_bp', __name__)

@analysis_bp.route("/analysis_api", methods=["POST"])
def analysis_api():
    data = request.get_json()
    symbol = data.get("symbol")
    indicators = data.get("indicators", [])

    df = yf.download(symbol, period="3mo", interval="1d")

    result = {}

    # ===================== EMA =====================
    if "ema" in indicators:
        df["EMA_20"] = df["Close"].ewm(span=20, adjust=False).mean()
        result["ema"] = {
            "value": round(df["EMA_20"].iloc[-1], 3)
        }

    # ===================== Bollinger Bands =====================
    if "bollinger" in indicators:
        df["MA20"] = df["Close"].rolling(window=20).mean()
        df["STD20"] = df["Close"].rolling(window=20).std()

        df["Upper"] = df["MA20"] + (df["STD20"] * 2)
        df["Lower"] = df["MA20"] - (df["STD20"] * 2)

        result["bollinger"] = {
            "upper": round(df["Upper"].iloc[-1], 3),
            "middle": round(df["MA20"].iloc[-1], 3),
            "lower": round(df["Lower"].iloc[-1], 3)
        }

    return jsonify(result)
analysis_bp = Blueprint("analysis_bp", __name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@analysis_bp.route("/analysis")
def analysis_page():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("analysis.html")

@analysis_bp.route("/analysis/run", methods=["POST"])
def run_analysis():
    data = request.get_json()
    symbol = data["symbol"]

    # تحليل ذكي بواسطة OpenAI
    prompt = f"حلل العملة {symbol} من حيث الاتجاه، الدعم، المقاومة، الفوليوم، والمحافظ الكبيرة."

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user", "content":prompt}]
    )

    ai_text = response.choices[0].message.content

    # حفظ التحليل في قاعدة البيانات
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO analysis (user_id, symbol, result) VALUES (?, ?, ?)",
                   (session["user_id"], symbol, ai_text))
    conn.commit()

    return jsonify({"ai": ai_text})
