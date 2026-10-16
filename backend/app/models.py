import json
from datetime import datetime, date
from . import db


def init_db():
    """Initialize database with sample data for Akpera Mill"""
    from .models import Product, Cart, Order

    # Create tables
    db.create_all()

    # Check if products already exist
    if Product.query.count() == 0:
        # Sample rice products based on the PDF mockups
        products = [
            {
                'name': 'Premium Long Grain',
                'slug': 'premium-long-grain',
                'description': 'Clean, beautifully separated grains for everyday meals and memorable occasions.',
                'price': 8500000,  # ₦85,000 in kobo
                'original_price': 10000000,
                'category': 'Rice',
                'subcategory': 'Long Grain',
                'brand': 'Akpera Mill',
                'rating': 4.8,
                'review_count': 128,
                'stock_status': 'in_stock',
                'sku': 'AK-LG-50KG',
                'weight': '50kg',
                'dimensions': '50cm × 30cm × 10cm',
                'image_main': 'product-1-main.jpg',
                'image_gallery': json.dumps(['product-1-1.jpg', 'product-1-2.jpg', 'product-1-3.jpg']),
                'specs': json.dumps({
                    'grain_type': 'Long Grain',
                    'purity': '99.9%',
                    'moisture_content': '13% max',
                    'origin': 'Nigeria',
                    'harvest_batch': 'October 2026'
                }),
                'tags': json.dumps(['premium', 'long-grain', 'best-seller']),
                'is_featured': True
            },
            {
                'name': 'Golden Parboiled',
                'slug': 'golden-parboiled',
                'description': 'Premium parboiled rice with golden kernel color and enhanced nutrition.',
                'price': 4400000,  # ₦44,000 in kobo
                'original_price': 5500000,
                'category': 'Rice',
                'subcategory': 'Parboiled',
                'brand': 'Akpera Mill',
                'rating': 4.8,
                'review_count': 97,
                'stock_status': 'in_stock',
                'sku': 'AK-GP-25KG',
                'weight': '25kg',
                'dimensions': '35cm × 25cm × 10cm',
                'image_main': 'product-2-main.jpg',
                'image_gallery': json.dumps(['product-2-1.jpg', 'product-2-2.jpg']),
                'specs': json.dumps({
                    'grain_type': 'Parboiled',
                    'purity': '99.5%',
                    'parboiling': 'Steam pressure process',
                    'origin': 'Nigeria'
                }),
                'tags': json.dumps(['parboiled', 'golden', 'nutrition']),
                'is_featured': False
            },
            {
                'name': 'Aromatic Fragrant',
                'slug': 'aromatic-fragrant',
                'description': 'Aromatic rice variety with natural fragrance and excellent cooking quality.',
                'price': 2400000,  # ₦24,000 in kobo
                'original_price': 3000000,
                'category': 'Rice',
                'subcategory': 'Fragrant',
                'brand': 'Akpera Mill',
                'rating': 4.8,
                'review_count': 3500,
                'stock_status': 'in_stock',
                'sku': 'AK-AF-10KG',
                'weight': '10kg',
                'dimensions': '20cm × 15cm × 5cm',
                'image_main': 'product-3-main.jpg',
                'image_gallery': json.dumps(['product-3-1.jpg', 'product-3-2.jpg', 'product-3-3.jpg']),
                'specs': json.dumps({
                    'grain_type': 'Fragrant',
                    'aroma': 'Natural aged aroma',
                    'purity': '99.8%',
                    'origin': 'Nigeria'
                }),
                'tags': json.dumps(['fragrant', 'aromatic', 'everyday']),
                'is_featured': False
            },
            {
                'name': 'Brown Rice',
                'slug': 'brown-rice',
                'description': 'Wholegrain brown rice with bran layer for maximum fiber and nutrients.',
                'price': 1350000,  # ₦13,500 in kobo
                'original_price': 1800000,
                'category': 'Rice',
                'subcategory': 'Brown',
                'brand': 'Akpera Mill',
                'rating': 4.8,
                'review_count': 210,
                'stock_status': 'low_stock',
                'sku': 'AK-BR-5KG',
                'weight': '5kg',
                'dimensions': '12cm × 8cm × 4cm',
                'image_main': 'product-4-main.jpg',
                'image_gallery': json.dumps(['product-4-1.jpg', 'product-4-2.jpg']),
                'specs': json.dumps({
                    'grain_type': 'Brown',
                    'fiber_content': '8g per serving',
                    'purity': '99%',
                    'origin': 'Nigeria'
                }),
                'tags': json.dumps(['brown', 'wholegrain', 'healthy']),
                'is_featured': False
            },
            {
                'name': 'Premium Long Grain (25kg)',
                'slug': 'premium-long-grain-25kg',
                'description': 'Premium long grain rice in 25kg bag for medium-sized families.',
                'price': 4300000,  # ₦43,000 in kobo
                'original_price': 5000000,
                'category': 'Rice',
                'subcategory': 'Long Grain',
                'brand': 'Akpera Mill',
                'rating': 4.8,
                'review_count': 89,
                'stock_status': 'in_stock',
                'sku': 'AK-LG-25KG',
                'weight': '25kg',
                'dimensions': '35cm × 25cm × 10cm',
                'image_main': 'product-5-main.jpg',
                'image_gallery': json.dumps(['product-5-1.jpg', 'product-5-2.jpg']),
                'specs': json.dumps({
                    'grain_type': 'Long Grain',
                    'purity': '99.9%',
                    'origin': 'Nigeria'
                }),
                'tags': json.dumps(['premium', 'long-grain', '25kg']),
                'is_featured': False
            },
            {
                'name': 'Parboiled 50kg',
                'slug': 'parboiled-50kg',
                'description': 'Value pack parboiled rice - best for large families and businesses.',
                'price': 8600000,  # ₦86,000 in kobo
                'original_price': 9500000,
                'category': 'Rice',
                'subcategory': 'Parboiled',
                'brand': 'Akpera Mill',
                'rating': 4.8,
                'review_count': 67,
                'stock_status': 'in_stock',
                'sku': 'AK-PB-50KG',
                'weight': '50kg',
                'dimensions': '50cm × 35cm × 12cm',
                'image_main': 'product-6-main.jpg',
                'image_gallery': json.dumps(['product-6-1.jpg', 'product-6-2.jpg', 'product-6-3.jpg']),
                'specs': json.dumps({
                    'grain_type': 'Parboiled',
                    'purity': '99.5%',
                    'parboiling': 'Steam pressure process',
                    'origin': 'Nigeria',
                    'harvest_batch': 'October 2026'
                }),
                'tags': json.dumps(['parboiled', 'value-pack', '50kg']),
                'is_featured': False
            },
        ]

        for prod_data in products:
            product = Product(**prod_data)
            db.session.add(product)

        db.session.commit()
        print(f"Initialized {len(products)} products")


def get_product_by_slug(slug):
    """Get product by slug"""
    from .models import Product
    return Product.query.filter_by(slug=slug).first_or_404()


def get_products_by_category(category, page=1, per_page=12):
    """Get products by category with pagination"""
    from .models import Product
    query = Product.query.filter_by(category=category, stock_status='in_stock')
    return query.paginate(page=page, per_page=per_page, error_out=False)


def search_products(query, page=1, per_page=12):
    """Search products by name or tags"""
    from .models import Product
    search = f'%{query}%'
    products = Product.query.filter(
        (Product.name.ilike(search)) |
        (Product.tags.ilike(f'%{query}%'))
    ).paginate(page=page, per_page=per_page, error_out=False)
    return products


def get_filter_options():
    """Get available filter options from product database"""
    from .models import Product

    grains = db.session.query(Product.subcategory).filter(
        Product.subcategory.isnot(None)
    ).distinct().all()
    grain_types = [g[0] for g in grains if g[0]]

    sizes = db.session.query(Product.weight).filter(
        Product.weight.isnot(None)
    ).distinct().all()
    bag_sizes = [s[0] for s in sizes if s[0]]

    return {
        'grain_types': grain_types,
        'bag_sizes': bag_sizes
    }