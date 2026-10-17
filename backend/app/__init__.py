import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix
from itsdangerous import Serializer

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///akpera_mill.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['WTF_CSRF_TIME_LIMIT'] = 3600
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from .api import api_bp
    from .main import main_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(main_bp)
    
    return app

__all__ = ['create_app', 'db', 'migrate']
