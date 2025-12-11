import os
import importlib
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ROUTES_FOLDER = "backend/routes"

def register_all_routes():
    for filename in os.listdir(ROUTES_FOLDER):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            module_path = f"backend.routes.{module_name}"

            try:
                module = importlib.import_module(module_path)

                # تسجيل كل Blueprints تلقائيًا
                for attr in dir(module):
                    obj = getattr(module, attr)
                    if hasattr(obj, "route") and hasattr(obj, "register"):
                        app.register_blueprint(obj, url_prefix="/api")
                        print(f"🔵 Registered: {module_name}.{attr}")

            except Exception as e:
                print(f"❌ Error importing {module_path}: {e}")

register_all_routes()

@app.route("/")
def home():
    return "🚀 Backend running with auto route loader!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)     
