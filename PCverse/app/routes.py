from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Product, Category, Build, BuildItem
from app.compatibility import check_build_compatibility
from app.power_calculator import calculate_build_power
from app.performance_recommendation import check_cpu_gpu_performance
from app.usage_recommendation import get_usage_recommendation
from app.performance import check_cpu_gpu_performance

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

    # =========================
    # DUPLICATE COMPONENT CHECK
    # =========================

    warnings = {}

    for item in build.items:

        category = item.product.category.name

        if category not in warnings:
            warnings[category] = []

        warnings[category].append(item)

    duplicate_warnings = {}

    for category, items in warnings.items():

        if len(items) > 1:
            duplicate_warnings[category] = items

    # =========================
    # COMPATIBILITY CHECK
    # =========================

    compatibility_result = check_build_compatibility(build)

    # =========================
    # FIND CPU AND GPU
    # =========================

    cpu = None
    gpu = None

    for item in build.items:

        category = item.product.category.name

        if category == "CPU":
            cpu = item.product

        elif category == "GPU":
            gpu = item.product

    # =========================
    # CPU ↔ GPU PERFORMANCE
    # =========================

    performance_result = None

    if cpu and gpu:
        performance_result = check_cpu_gpu_performance(cpu, gpu)

    # =========================
    # POWER CALCULATION
    # =========================

    power_result = calculate_build_power(build)

    # =========================
    # USAGE RECOMMENDATION
    # =========================

    usage = request.args.get("usage")

    usage_result = None

    if usage:
        usage_result = get_usage_recommendation(build, usage)

    # =========================
    # TOTAL PRICE
    # =========================

    total_price = 0

    for item in build.items:
        total_price += item.product.price

    # =========================
    # RENDER PAGE
    # =========================

    return render_template(
        "build.html",
        build=build,
        duplicate_warnings=duplicate_warnings,
        compatibility_result=compatibility_result,
        power_result=power_result,
        performance_result=performance_result,
        usage=usage,
        usage_result=usage_result,
        total_price=total_price
    )

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
