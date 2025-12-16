# backend/app.py
import os
import importlib
from flask import Flask, Blueprint
from flask_cors import CORS

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(
    __name__,
    template_folder=TEMPLATES_DIR,
    static_folder=STATIC_DIR,
    static_url_path="/static"
)
CORS(app)

ROUTES_FOLDER = os.path.join(os.path.dirname(__file__), "routes")

def register_all_blueprints():
    for filename in os.listdir(ROUTES_FOLDER):
        if not filename.endswith(".py") or filename.startswith("__"):
            continue

        module_name = filename[:-3]
        module_path = f"backend.routes.{module_name}"

        try:
            module = importlib.import_module(module_path)
        except Exception as e:
            print(f"❌ Skipping {module_path}: {e}")
            continue

        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, Blueprint):
                try:
                    app.register_blueprint(attr)
                    print(f"✅ Registered {module_path}.{attr_name}")
                except Exception as e:
                    print(f"❌ Could not register {module_path}.{attr_name}: {e}")

register_all_blueprints()

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
