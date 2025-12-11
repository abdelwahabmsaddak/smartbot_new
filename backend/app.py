import os
import importlib
from flask import Flask, Blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# المسار الفعلي لمجلد الروتات
ROUTES_FOLDER = os.path.join(os.path.dirname(__file__), "routes")


def register_all_blueprints():
    """
    يبحث في backend/routes عن أي Blueprint حقيقي
    ويسجّله في التطبيق. يتجاهل أي خطأ في الاستيراد.
    """
    for filename in os.listdir(ROUTES_FOLDER):
        # نتجاهل الملفات الغير بايثون أو __init__.py
        if not filename.endswith(".py") or filename == "__init__.py":
            continue

        module_name = filename[:-3]
        module_path = f"backend.routes.{module_name}"

        try:
            module = importlib.import_module(module_path)
        except Exception as e:
            # هنا فقط نطبع الخطأ، لكن ما نوقفش التطبيق
            print(f"❌ Skipping {module_path}: {e}")
            continue

        # نبحث عن المتغيّرات اللي هي Blueprint
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, Blueprint):
                try:
                    app.register_blueprint(attr, url_prefix="/api")
                    print(f"✅ Registered {module_path}.{attr_name}")
                except Exception as e:
                    print(
                        f"❌ Could not register {module_path}.{attr_name}: {e}"
                    )


# تسجيل كل الـ Blueprints
register_all_blueprints()


@app.route("/")
def home():
    return "🚀 Backend running successfully (auto blueprints)!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
