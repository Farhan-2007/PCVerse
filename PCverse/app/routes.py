from flask import Blueprint, render_template
from app.models import Product, Category

main = Blueprint('main', __name__)

# Home Page

@main.route("/")
def home():

    products = Product.query.order_by(Product.name.asc()).all()

    return render_template(
        "home.html",
        products=products
    )

# All Products

@main.route("/products")
def products():

    products = Product.query.order_by(Product.name.asc()).all()

    categories = Category.query.all()

    return render_template(
        "products.html",
        products=products,
        categories=categories
    )

# Product Details

@main.route("/product/<int:product_id>")
def product(product_id):

    product = Product.query.get_or_404(product_id)

    return render_template(
        "product.html",
        product=product
    )

# Category Products

@main.route("/category/<int:category_id>")
def category_products(category_id):

    category = Category.query.get_or_404(category_id)

    products = Product.query.filter_by(
        category_id=category_id
    ).order_by(Product.name.asc()).all()

    return render_template(
        "category.html",
        category=category,
        products=products
    )