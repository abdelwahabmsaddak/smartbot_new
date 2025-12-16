import os
import importlib
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "super-secret-key"
CORS(app)

# مسار routes
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
            try:
                from flask import Blueprint
                if isinstance(attr, Blueprint):
                    app.register_blueprint(attr)
                    print(f"✅ Registered {attr.name}")
            except Exception as e:
                print(f"❌ Blueprint error: {e}")

register_all_blueprints()

@app.route("/")
def home():
    return "🚀 SmartTrade AI Backend Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
