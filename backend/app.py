from flask import Flask
from flask_cors import CORS
from database import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URL
    app.config['SECRET_KEY'] = Config.SECRET_KEY

    CORS(app)
    db.init_app(app)

    # Import routes
    from routes.auth import auth_bp
    from routes.payments import payments_bp
    from routes.analysis import analysis_bp
    from routes.whales import whales_bp
    from routes.blog import blog_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(payments_bp, url_prefix="/api/pay")
    app.register_blueprint(analysis_bp, url_prefix="/api/analyze")
    app.register_blueprint(whales_bp, url_prefix="/api/whales")
    app.register_blueprint(blog_bp, url_prefix="/api/blog")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
