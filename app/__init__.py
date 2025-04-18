from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
import os

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/movie_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Create uploads folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Import models and register blueprints
    with app.app_context():
        from app import models
        db.create_all()
        from app.views import main
        app.register_blueprint(main)
    
    return app