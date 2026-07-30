from flask import Blueprint, render_template
from app.models import Product, Category

main = Blueprint("main", __name__)

# ================= HOME =================

@main.route("/")
def home():

    featured_products = Product.query.order_by(Product.name.asc()).limit(8).all()

    return render_template(
        "home.html",
        products=featured_products
    )


# ================= ALL PRODUCTS =================

@main.route("/products")
def products():

    products = Product.query.order_by(Product.name.asc()).all()

    categories = Category.query.order_by(Category.name.asc()).all()

    return render_template(
        "products.html",
        products=products,
        categories=categories
    )


# ================= PRODUCT DETAILS =================

@main.route("/product/<int:product_id>")
def product(product_id):

    product = Product.query.get_or_404(product_id)

    return render_template(
        "product.html",
        product=product
    )


# ================= CATEGORY PRODUCTS =================

@main.route("/category/<int:category_id>")
def category_products(category_id):

    category = Category.query.get_or_404(category_id)

    products = Product.query.filter_by(
        category_id=category.id
    ).order_by(Product.name.asc()).all()

    return render_template(
        "category.html",
        category=category,
        products=products
    )