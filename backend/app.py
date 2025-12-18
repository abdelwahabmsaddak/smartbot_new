import os
from flask import Flask
from flask_cors import CORS
from flask import render_template

@app.route("/")
def home():
    return render_template("dashboard.html")
# Flask App
app = Flask(__name__)
app.secret_key = "super-secret-key"
CORS(app)

# ===============================
# Register Blueprints MANUALLY
# ===============================

from backend.routes.dashboard import dashboard_bp

app.register_blueprint(
    dashboard_bp,
    url_prefix="/api/dashboard"
)

# ===============================
# Run App (local / render)
# ===============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
