import os
from flask import Flask, render_template
from flask_cors import CORS

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.secret_key = os.environ.get("SECRET_KEY", "super-secret-key")
    CORS(app)

    # ✅ Register blueprints (بدون importlib scanning باش ما يطيحش)
    from backend.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")

    # ✅ صفحات الواجهة
    @app.get("/")
    def home():
        # خليه يفتح dashboard مباشرة
        return render_template("dashboard.html")

    @app.get("/dashboard")
    def dashboard_page():
        return render_template("dashboard.html")

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
