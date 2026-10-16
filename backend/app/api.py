from flask import Blueprint, request, jsonify, session
from . import db
from .models import Product, Cart, Order, init_db, get_product_by_slug, get_products_by_category, search_products, get_filter_options
import json
import datetime

api_bp = Blueprint('api', __name__)


@api_bp.route('/products')
def list_products():
    """List all products with filtering and pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    category = request.args.get('category', type=str)
    search = request.args.get('search', type=str)
    grain_type = request.args.get('grain_type', type=str)
    bag_size = request.args.get('bag_size', type=str)
    min_price = request.args.get('min_price', type=int, default=0)
    max_price = request.args.get('max_price', type=int, default=999999999)
    stock = request.args.get('stock', type=str)

    query = Product.query

    if category:
        query = query.filter_by(category=category)
    if grain_type:
        query = query.filter_by(subcategory=grain_type)
    if bag_size:
        query = query.filter(Product.weight.like(f'%{bag_size}%'))
    if stock:
        query = query.filter_by(stock_status=stock)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if search:
        search_term = f'%{search}%'
        query = query.filter(
            (Product.name.ilike(search_term)) |
            (Product.tags.ilike(f'%{search}%'))
        )

    paginate = query.paginate(page=page, per_page=per_page, error_out=False)
    products = [prod.to_dict() for prod in paginate.items]

    return jsonify({
        'products': products,
        'total': paginate.total,
        'pages': paginate.pages,
        'page': paginate.page,
        'per_page': paginate.per_page,
        'has_next': paginate.has_next,
        'has_prev': paginate.has_prev
    })


@api_bp.route('/product/<slug>')
def product_detail(slug):
    """Get single product details"""
    product = get_product_by_slug(slug)
    return jsonify(product.to_dict())


@api_bp.route('/product/<slug>/similar')
def similar_products(slug):
    """Get similar products"""
    product = get_product_by_slug(slug)
    similar = get_similar_products(product.id)
    return jsonify(similar)


@api_bp.route('/cart', methods=['GET'])
def cart_view():
    """View cart"""
    from . import get_or_create_cart
    cart = get_or_create_cart()
    return jsonify(cart.to_dict())


@api_bp.route('/cart', methods=['POST'])
def cart_add():
    """Add item to cart"""
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    from . import get_or_create_cart
    cart = get_or_create_cart()

    # Parse existing items
    items = json.loads(cart.items) if cart.items else []

    # Check if product already in cart
    found = False
    for item in items:
        if item.get('id') == int(product_id):
            item['quantity'] = min(item.get('quantity', 0) + quantity, 10)
            found = True
            break

    if not found:
        product = Product.query.get(int(product_id))
        if product:
            items.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'weight': product.weight,
                'quantity': quantity
            })

    cart.items = json.dumps(items)
    db.session.commit()

    return jsonify(cart.to_dict())


@api_bp.route('/cart/remove', methods=['POST'])
def cart_remove():
    """Remove item from cart"""
    data = request.get_json()
    product_id = data.get('product_id')

    from . import get_or_create_cart
    cart = get_or_create_cart()

    items = json.loads(cart.items) if cart.items else []
    items = [item for item in items if item.get('id') != int(product_id)]
    cart.items = json.dumps(items)
    db.session.commit()

    return jsonify(cart.to_dict())


@api_bp.route('/cart/update', methods=['POST'])
def cart_update():
    """Update cart item quantity"""
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 0)

    from . import get_or_create_cart
    cart = get_or_create_cart()

    items = json.loads(cart.items) if cart.items else []
    for item in items:
        if item.get('id') == int(product_id):
            if quantity > 0:
                item['quantity'] = quantity
            else:
                items.remove(item)
            break

    cart.items = json.dumps(items)
    db.session.commit()

    return jsonify(cart.to_dict())


@api_bp.route('/checkout', methods=['POST'])
def checkout():
    """Create order from cart"""
    data = request.get_json()
    from . import get_or_create_cart, save_order

    cart = get_or_create_cart()

    items = json.loads(cart.items) if cart.items else []
    if not items:
        return jsonify({'error': 'Cart is empty'}), 400

    # Calculate totals
    subtotal = sum(item.get('price', 0) * item.get('quantity', 0) for item in items)
    delivery_fee = data.get('delivery_fee', 500000)  # ₦5,000 in kobo
    discount = data.get('discount', 0)

    total = subtotal + delivery_fee - discount

    # Generate order number
    order_number = f'AK-{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}-{hash(str(items)) % 10000:04d}'

    # Get user info from form data
    user_name = data.get('user_name', '')
    user_email = data.get('user_email', '')
    user_phone = data.get('user_phone', '')
    delivery_address = data.get('delivery_address', '')

    order = Order(
        order_number=order_number,
        user_name=user_name,
        user_email=user_email,
        user_phone=user_phone,
        subtotal=subtotal,
        delivery_fee=delivery_fee,
        discount_amount=discount,
        total=total,
        payment_method=data.get('payment_method', 'card'),
        delivery_address=delivery_address,
        notes=data.get('notes', '')
    )

    db.session.add(order)

    # Clear cart
    cart.items = json.dumps([])
    db.session.commit()

    return jsonify({
        'order': order.to_dict(),
        'cart_empty': True
    })


@api_bp.route('/orders')
def list_orders():
    """List orders (for user account)"""
    from .models import Order
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    paginate = Order.query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    orders = [order.to_dict() for order in paginate.items]

    return jsonify({
        'orders': orders,
        'total': paginate.total,
        'pages': paginate.pages,
        'page': paginate.page
    })


@api_bp.route('/filters/options')
def filter_options():
    """Get filter options for catalog"""
    options = get_filter_options()
    return jsonify(options)