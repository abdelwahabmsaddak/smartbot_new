from flask import Blueprint, request, session, jsonify, render_template
import sqlite3
import openai

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
