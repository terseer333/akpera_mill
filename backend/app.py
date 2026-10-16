import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_object='config.DevelopmentConfig'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .main import main_bp
    from .api import api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    # Static file serving
    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory('static', filename)

    # Error handlers
    @app.errorhandler(404)
    not_found_error(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    internal_error(e):
        return render_template('500.html'), 500

    return app


# Database Models
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)  # in kobo/cents
    original_price = db.Column(db.Integer)  # in kobo/cents
    category = db.Column(db.String(100))
    subcategory = db.Column(db.String(100))
    brand = db.Column(db.String(100), default='Akpera Mill')
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    stock_status = db.Column(db.String(20), default='in_stock')  # in_stock, low_stock, out_of_stock
    sku = db.Column(db.String(50), unique=True, nullable=False)
    weight = db.Column(db.String(50))  # e.g., "50kg", "25kg", "10kg", "5kg"
    dimensions = db.Column(db.String(100))
    image_main = db.Column(db.String(200))
    image_gallery = db.Column(db.Text)  # JSON string of additional images
    specs = db.Column(db.Text)  # JSON string of specifications
    tags = db.Column(db.Text)  # JSON string of tags
    is_featured = db.Column(db.Boolean, default=False)
    date_added = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'price': self.price,
            'original_price': self.original_price,
            'category': self.category,
            'subcategory': self.subcategory,
            'brand': self.brand,
            'rating': self.rating,
            'review_count': self.review_count,
            'stock_status': self.stock_status,
            'sku': self.sku,
            'weight': self.weight,
            'dimensions': self.dimensions,
            'image_main': self.image_main,
            'image_gallery': self.image_gallery,
            'specs': self.specs,
            'tags': self.tags,
            'is_featured': self.is_featured,
            'date_added': self.date_added.isoformat() if self.date_added else None
        }


class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False, unique=True)
    items = db.Column(db.Text)  # JSON string of cart items
    created_at = db.Column(db.DateTime, default=db.func.now)
    updated_at = db.Column(db.DateTime, default=db.func.now, onupdate=db.func.now)

    def to_dict(self):
        import json
        items = json.loads(self.items) if self.items else []
        return {
            'id': self.id,
            'session_id': self.session_id,
            'items': items,
            'item_count': sum(item.get('quantity', 0) for item in items),
            'total_price': sum(item.get('price', 0) * item.get('quantity', 0) for item in items)
        }


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    user_email = db.Column(db.String(120))
    user_name = db.Column(db.String(100))
    user_phone = db.Column(db.String(50))
    subtotal = db.Column(db.Integer, nullable=False)  # in kobo/cents
    delivery_fee = db.Column(db.Integer, default=0)  # in kobo/cents
    discount_amount = db.Column(db.Integer, default=0)  # in kobo/cents
    total = db.Column(db.Integer, nullable=False)  # in kobo/cents
    status = db.Column(db.String(20), default='pending')  # pending, processing, shipped, delivered, cancelled
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(20), default='pending')  # pending, completed, failed, refunded
    delivery_address = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now)
    updated_at = db.Column(db.DateTime, default=db.func.now, onupdate=db.func.now)

    def to_dict(self):
        import json
        return {
            'id': self.id,
            'order_number': self.order_number,
            'user_email': self.user_email,
            'user_name': self.user_name,
            'user_phone': self.user_phone,
            'subtotal': self.subtotal,
            'delivery_fee': self.delivery_fee,
            'discount_amount': self.discount_amount,
            'total': self.total,
            'status': self.status,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'delivery_address': self.delivery_address,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# Config class
class DevelopmentConfig:
    """Development configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///akpera_mill.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # Set to False in production
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600


class ProductionConfig:
    """Production configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change-me'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///akpera_mill.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    ENV = 'production'


# Helper functions
def get_categories():
    """Get all product categories from database"""
    from .models import Product
    categories = db.session.query(Product.category).filter(
        Product.category.isnot(None)
    ).distinct().all()
    return [cat[0] for cat in categories if cat[0]]


def get_bestsellers(limit=8):
    """Get bestselling products"""
    from .models import Product
    products = Product.query.filter_by(is_featured=True).limit(limit).all()
    return [prod.to_dict() for prod in products]


def get_similar_products(product_id, limit=4):
    """Get similar products based on category"""
    from .models import Product
    product = Product.query.get(product_id)
    if not product:
        return []
    products = Product.query.filter(
        Product.category == product.category,
        Product.id != product_id,
        Product.stock_status == 'in_stock'
    ).limit(limit).all()
    return [prod.to_dict() for prod in products]


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)