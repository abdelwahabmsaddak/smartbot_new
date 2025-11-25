from flask import Flask, render_template, redirect, session
from auth import auth_bp
from routes.admin import admin_bp
from routes.profile import profile_bp
from routes.usage import usage_bp
from routes.chatbot import chatbot_bp
from routes.payments import payments_bp        # إن وجد
from routes.billing import billing_bp          # إن وجد
from routes.affiliate import affiliate_bp      # صفحة الافلييت
from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)


# === عرض إدارة المدونة ===
@app.route("/admin/blog")
def admin_blog():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()
    return render_template("admin_blog.html", posts=posts)


# === إنشاء مقال ===
@app.route("/admin/blog/create", methods=["POST"])
def create_post():
    title = request.form["title"]
    content = request.form["content"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO posts (title, content, created_at, updated_at) VALUES (?, ?, ?, ?)",
              (title, content, now, now))
    conn.commit()
    conn.close()

    return redirect("/admin/blog")


# === تعديل مقال ===
@app.route("/admin/blog/edit/<int:id>")
def edit_post(id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id=?", (id,))
    post = c.fetchone()
    conn.close()
    return render_template("edit_post.html", post=post)


@app.route("/admin/blog/edit/<int:id>", methods=["POST"])
def save_edit_post(id):
    title = request.form["title"]
    content = request.form["content"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("UPDATE posts SET title=?, content=?, updated_at=? WHERE id=?",
              (title, content, now, id))
    conn.commit()
    conn.close()

    return redirect("/admin/blog")


# === حذف مقال ===
@app.route("/admin/blog/delete/<int:id>")
def delete_post(id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM posts WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/admin/blog")
app = Flask(__name__)
app.secret_key = "SECRET_KEY"   # بدّلها فيما بعد


# ==============================
# 📌 تسجيل جميع البلوبرنت
# ==============================

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(usage_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(affiliate_bp)

# لو عندك payments و billing
try:
    app.register_blueprint(payments_bp)
    app.register_blueprint(billing_bp)
except:
    pass


# ==============================
# 📌 الروت الرئيسي — الصفحة الرئيسية
# ==============================

@app.route('/')
def home():
    return render_template('index.html')


# ==============================
# 📌 الداشبورد للمستخدم بعد الدخول
# ==============================

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('dashboard.html')


# ==============================
# 📌 تشغيل السيرفر
# ==============================

if __name__ == '__main__':
    app.run(debug=True)
