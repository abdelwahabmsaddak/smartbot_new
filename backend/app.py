from flask import Flask, render_template, session, redirect
from auth import auth_bp
from routes.admin import admin_bp
from routes.profile import profile_bp
app = Flask(__name__)
app.secret_key = "SECRET_KEY"

app.register_blueprint(auth_bp)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('dashboard.html')

@app.route('/')
def home():
    return render_template('index.html')
app.register_blueprint(admin_bp)
if __name__ == '__main__':
    app.run(debug=True)
app.register_blueprint(profile_bp)
