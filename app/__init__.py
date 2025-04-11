from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # App config
    app.config['SECRET_KEY'] = 'super-secret-key'  # Change to a secure one in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:your_password@localhost/BLOOD_MANAGEMENT_SYSTEM'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect to login page if not authenticated

    # Import and register blueprints
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from .routes.recipient import recipient_bp
    app.register_blueprint(recipient_bp)

    from .routes.donor import donor_bp
    app.register_blueprint(donor_bp)

    from .routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    return app

