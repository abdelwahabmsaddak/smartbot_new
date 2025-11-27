from flask import Blueprint, render_template, request, redirect, session
import sqlite3
import openai

blog_bp = Blueprint("blog_bp", __name__)

def get_db():
    return sqlite3.connect("database.db")

@blog_bp.route("/blog")
def blog():
    db = get_db()
    posts = db.execute("SELECT id,title,content,date FROM blog ORDER BY id DESC").fetchall()
    db.close()
    return render_template("blog.html", posts=posts)

@blog_bp.route("/blog/new", methods=["POST"])
def new_post():
    title = request.form["title"]
    content = request.form["content"]

    db = get_db()
    db.execute("INSERT INTO blog (title, content, date) VALUES (?, ?, datetime('now'))",
               (title, content))
    db.commit()
    db.close()
    return redirect("/blog")

# كتابة تدوينة بالذكاء الاصطناعي
@blog_bp.route("/blog/ai_generate", methods=["POST"])
def ai_generate():
    topic = request.form["topic"]

    prompt = f"اكتب مقالة عربية احترافية عن: {topic}"

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]
