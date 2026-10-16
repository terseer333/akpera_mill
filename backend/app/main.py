from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from . import db
from .models import Product, init_db, get_products_by_category, search_products, get_filter_options, get_bestsellers, Cart
import json

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """Home page"""
    init_db()
    bestsellers = get_bestsellers(8)
    filter_options = get_filter_options()
    # Get featured products from each category
    featured = Product.query.filter_by(is_featured=True).limit(4).all()
    return render_template('home.html',
                           bestsellers=[p.to_dict() for p in bestsellers],
                           filter_options=filter_options,
                           featured=[p.to_dict() for p in featured])


@main_bp.route('/catalog')
def catalog():
    """Catalog page with filtering"""
    init_db()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)

    category = request.args.get('category', type=str)
    grain_type = request.args.get('grain_type', type=str)
    bag_size = request.args.get('bag_size', type=str)
    min_price = int(request.args.get('min_price', 0) or 0)
    max_price = int(request.args.get('max_price', 999999999) or 999999999)
    stock = request.args.get('stock', type=str)

    query = get_products_by_category(category, page, per_page) if category else None

    if not category:
        products = search_products(
            request.args.get('search', '', type=str),
            page, per_page
        ) if request.args.get('search') else Product.query.paginate(
            page=page, per_page=per_page, error_out=False
        ).items
        total = len(Product.query.all())
    else:
        products = query.items
        total = query.total

    filter_options = get_filter_options()

    # Apply additional filters
    if grain_type:
        products = [p for p in products if p.get('subcategory') == grain_type]
    if bag_size:
        products = [p for p in products if bag_size in (p.get('weight', '') or '')]
    if stock:
        products = [p for p in products if p.get('stock_status') == stock]

    # Price filtering
    if min_price or max_price:
        products = [p for p in products if min_price <= p.get('price', 0) <= max_price]

    # Calculate price range for filter UI
    all_products = Product.query.filter(Product.stock_status == 'in_stock').all()
    prices = [p.price for p in all_products]
    price_range = {
        'min': min(prices) if prices else 0,
        'max': max(prices) if prices else 10000000
    }

    return render_template('catalog.html',
                           products=products,
                           total=total,
                           page=page,
                           per_page=per_page,
                           filter_options=filter_options,
                           price_range=price_range,
                           selected_category=category,
                           selected_grain=grain_type,
                           selected_size=bag_size,
                           selected_stock=stock)


@main_bp.route('/product/<slug>')
def product_detail(slug):
    """Product detail page"""
    init_db()
    product = get_product_by_slug(slug)

    # Get similar products
    similar = get_similar_products(product.id)

    return render_template('product_detail.html',
                           product=product.to_dict(),
                           similar=similar)


@main_bp.route('/cart')
def cart():
    """Shopping cart page"""
    init_db()
    from . import get_or_create_cart
    cart = get_or_create_cart()
    return render_template('cart.html', cart=cart.to_dict())


@main_bp.route('/checkout/delivery', methods=['GET', 'POST'])
def checkout_delivery():
    """Delivery step of checkout"""
    init_db()
    from . import get_or_create_cart
    cart = get_or_create_cart()

    if request.method == 'POST':
        # Save delivery details to session
        session['delivery_address'] = request.form.get('address', '')
        session['delivery_notes'] = request.form.get('notes', '')
        return jsonify({'success': True})

    return render_template('checkout_delivery.html', cart=cart.to_dict())


@main_bp.route('/checkout/payment', methods=['GET', 'POST'])
def checkout_payment():
    """Payment step of checkout"""
    init_db()
    from . import get_or_create_cart
    cart = get_or_create_cart()

    if request.method == 'POST':
        payment_method = request.form.get('payment_method', 'card')
        session['payment_method'] = payment_method
        return jsonify({'success': True})

    return render_template('checkout_payment.html', cart=cart.to_dict())


@main_bp.route('/checkout/review')
def checkout_review():
    """Order review step of checkout"""
    init_db()
    from . import get_or_create_cart
    from .api import save_order

    cart = get_or_create_cart()
    items = json.loads(cart.items) if cart.items else []

    # Get order data from session or form
    delivery_address = session.get('delivery_address', '')
    payment_method = session.get('payment_method', 'card')

    # Calculate totals
    subtotal = sum(item.get('price', 0) * item.get('quantity', 0) for item in items)
    delivery_fee = 500000  # ₦5,000
    discount = 0
    total = subtotal + delivery_fee - discount

    order_number = f'AK-{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}'

    return render_template('checkout_review.html',
                           cart=cart.to_dict(),
                           items=items,
                           delivery_address=delivery_address,
                           payment_method=payment_method,
                           subtotal=subtotal,
                           delivery_fee=delivery_fee,
                           discount=discount,
                           total=total,
                           order_number=order_number)


@main_bp.route('/empty-cart')
def empty_cart():
    """Empty cart page"""
    init_db()
    from . import get_or_create_cart
    cart = get_or_create_cart()
    cart.items = json.dumps([])
    db.session.commit()
    return redirect(url_for('main.catalog'))


@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@main_bp.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')


# Helper: Get or create cart for session
def get_or_create_cart():
    """Get or create a cart for the current session"""
    from .models import Cart

    session_id = session.session_id

    cart = Cart.query.filter_by(session_id=session_id).first()
    if not cart:
        cart = Cart(session_id=session_id)
        db.session.add(cart)
        db.session.commit()

    return cart


# Helper: Get similar products
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