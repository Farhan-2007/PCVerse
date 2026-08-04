from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Product, Category, Build, BuildItem

main = Blueprint("main", __name__)


# ================= HOME =================

@main.route("/")
def home():

    featured_products = Product.query.order_by(Product.name.asc()).limit(8).all()

    return render_template("home.html", products=featured_products)

# ================= ALL PRODUCTS =================

@main.route("/products")
def products():

    build_id = request.args.get("build_id", type = int)

    products = Product.query.order_by(Product.name.asc()).all()

    categories = Category.query.order_by(Category.name.asc()).all()

    return render_template("products.html", build_id = build_id, products=products, categories=categories)

# ================= PRODUCT DETAILS =================

@main.route("/product/<int:product_id>")
def product(product_id):

    product = Product.query.get_or_404(product_id)

    build_id = request.args.get("build_id", type=int)

    return render_template("product.html", product=product, build_id = build_id)

# ================= CATEGORY PRODUCTS =================

@main.route("/category/<int:category_id>")
def category_products(category_id):

    category = Category.query.get_or_404(category_id)

    products = Product.query.filter_by(category_id=category.id).order_by(Product.name.asc()).all()

    build_id = request.args.get("build_id", type=int)

    return render_template("category.html",category=category,products=products)

# ================= MY BUILDS =================

@main.route("/my-builds")
@login_required
def my_builds():

    builds = Build.query.filter_by(user_id=current_user.id).all()
    return render_template("my_build.html",builds=builds)


# ================= CREATE BUILD =================

@main.route("/create-build", methods=["GET", "POST"])
@login_required
def create_build():

    if request.method == "POST":

        build_name = request.form.get("name")

        if build_name:

            new_build = Build(name=build_name, user_id=current_user.id)

            db.session.add(new_build)
            db.session.commit()

            return redirect(url_for("main.my_builds"))

    return render_template("create_build.html")

# ================= BUILD DETAILS =================
@main.route("/build/<int:build_id>")
@login_required
def build(build_id):

    build = Build.query.get_or_404(build_id)

    if build.user_id != current_user.id:
        return redirect(url_for("main.my_builds"))

    warnings = {}

    for item in build.items:

        category = item.product.category.name

        if category not in warnings:
            warnings[category] = []

        # Store the BuildItem instead of the Product
        warnings[category].append(item)

    duplicate_warnings = {}

    for category, items in warnings.items():

        if len(items) > 1:
            duplicate_warnings[category] = items

    total_price= 0;
    for items in build.items:
        total_price += items.product.price
    

    return render_template("build.html", build=build, duplicate_warnings=duplicate_warnings, total_price=total_price)

@main.route("/build/<int:build_id>/add/<int:product_id>")
@login_required
def add_to_build(build_id, product_id):

    build = Build.query.get_or_404(build_id)

    if build.user_id != current_user.id:
        return redirect(url_for("main.my_builds"))

    product = Product.query.get_or_404(product_id)

    existing_item = BuildItem.query.filter_by(
        build_id=build.id,
        product_id=product.id
    ).first()

    if existing_item:
        return redirect(url_for("main.build", build_id=build.id))

    new_item = BuildItem(
        build_id=build.id,
        product_id=product.id
    )

    db.session.add(new_item)
    db.session.commit()

    return redirect(url_for("main.build", build_id=build.id))

@main.route("/build/<int:build_id>/remove/<int:item_id>")
@login_required
def remove_from_build(build_id, item_id):

    build = Build.query.get_or_404(build_id)

    if build.user_id != current_user.id:
        return redirect(url_for("main.my_builds"))

    item = BuildItem.query.get_or_404(item_id)

    db.session.delete(item)
    db.session.commit()

    return redirect(url_for("main.build", build_id=build.id))
