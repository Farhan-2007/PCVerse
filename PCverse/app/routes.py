from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Product, Category, Build, BuildItem
from app.build_tools import make_virtual_build
from app.compatibility import check_build_compatibility
from app.power_calculator import calculate_build_power
from app.performance import check_cpu_gpu_performance
from app.usage_recommendation import get_usage_recommendation
from app.recommendation import recommend_components, USAGE_PROFILES
from app.build_tools import USAGE_LABELS, analyze_products, swap_options
from flask import flash, abort
from app.build_score import calculate_build_score
from app.upgrade_suggestions import get_upgrade_suggestions
from sqlalchemy import or_

main = Blueprint("main", __name__)

# HOME

@main.route("/")
def home():
    return render_template("home.html")

# ALL PRODUCTS

@main.route("/products")
def products():

    build_id = request.args.get(
        "build_id",
        type=int
    )

    search = request.args.get("search", "").strip()
    product_query = Product.query

    if search:
        pattern = f"%{search}%"
        product_query = product_query.filter(
            or_(
                Product.name.ilike(pattern),
                Product.brand.ilike(pattern)
            )
        )

    products = product_query.order_by(Product.name.asc()).all()

    categories = (
        Category.query
        .order_by(Category.name.asc())
        .all()
    )

    return render_template(
        "products.html",
        build_id=build_id,
        search=search,
        products=products,
        categories=categories
    )

# PRODUCT DETAILS

@main.route("/product/<int:product_id>")
def product(product_id):

    product = db.get_or_404(Product, product_id)

    build_id = request.args.get(
        "build_id",
        type=int
    )

    return render_template(
        "product.html",
        product=product,
        build_id=build_id
    )

# CATEGORY PRODUCTS

@main.route("/category/<int:category_id>")
def category_products(category_id):

    category = db.get_or_404(Category, category_id)

    products = (
        Product.query
        .filter_by(category_id=category.id)
        .order_by(Product.name.asc())
        .all()
    )

    build_id = request.args.get(
        "build_id",
        type=int
    )

    return render_template(
        "category.html",
        category=category,
        products=products,
        build_id=build_id
    )

# MY BUILDS

@main.route("/my-builds")
@login_required
def my_builds():

    builds = Build.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "my_build.html",
        builds=builds
    )

# CREATE BUILD

@main.route("/create-build", methods=["GET", "POST"])
@login_required
def create_build():

    if request.method == "POST":

        build_name = request.form.get("name", "").strip()

        if not build_name or len(build_name) > 100:
            flash("Enter a build name of 1 to 100 characters.", "error")
        else:

            new_build = Build(
                name=build_name,
                user_id=current_user.id
            )

            db.session.add(new_build)
            db.session.commit()

            return redirect(
                url_for("main.my_builds")
            )

    return render_template(
        "create_build.html"
    )

# BUILD DETAILS

@main.route("/build/<int:build_id>")
@login_required
def build(build_id):

    build = db.get_or_404(Build, build_id)

    if build.user_id != current_user.id:

        return redirect(
            url_for("main.my_builds")
        )

    # DUPLICATE COMPONENT CHECK

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

    compatibility_result = (
        check_build_compatibility(build)
    )

    cpu = None
    gpu = None

    for item in build.items:

        category = item.product.category.name

        if category == "CPU":

            cpu = item.product

        elif category == "GPU":

            gpu = item.product

    performance_result = None

    if cpu and gpu:

        performance_result = (
            check_cpu_gpu_performance(
                cpu,
                gpu
            )
        )


    power_result = calculate_build_power(
        build
    )

    usage = request.args.get(
        "usage"
    )

    usage_result = None

    if usage:

        usage_result = (
            get_usage_recommendation(
                build,
                usage
            )
        )

    total_price = 0

    for item in build.items:

        total_price += item.product.price


    upgrade_suggestions = get_upgrade_suggestions(
        build
    )

    return render_template(
        "build.html",

        build=build,

        duplicate_warnings=
            duplicate_warnings,

        compatibility_result=
            compatibility_result,

        power_result=
            power_result,

        performance_result=
            performance_result,

        usage=
            usage,

        usage_result=
            usage_result,

        total_price=
            total_price,

        upgrade_suggestions=upgrade_suggestions
    )

@main.route("/build/<int:build_id>/delete", methods=["POST"])
@login_required
def delete_build(build_id):

    build = db.get_or_404(Build, build_id)

    if build.user_id != current_user.id:
        abort(403)

    db.session.delete(build)
    db.session.commit()

    flash("Build deleted successfully.", "success")

    return redirect(url_for("main.my_builds"))

# REMOVE COMPONENT FROM BUILD

@main.route(
    "/build/<int:build_id>/remove/<int:item_id>",
    methods=["POST"]
)
@login_required
def remove_from_build(
    build_id,
    item_id
):

    build = db.get_or_404(Build, build_id)

    if build.user_id != current_user.id:

        return redirect(
            url_for("main.my_builds")
        )


    item = db.get_or_404(BuildItem, item_id)

    if item.build_id != build.id:

        return redirect(
            url_for(
                "main.build",
                build_id=build.id
            )
        )


    db.session.delete(item)

    db.session.commit()


    return redirect(
        url_for(
            "main.build",
            build_id=build.id
        )
    )

# ADD COMPONENT TO BUILD

@main.route(
    "/build/<int:build_id>/add/<int:product_id>",
    methods=["POST"]
)
@login_required
def add_to_build(
    build_id,
    product_id
):

    build = db.get_or_404(Build, build_id)

    if build.user_id != current_user.id:

        return redirect(
            url_for("main.my_builds")
        )


    product = db.get_or_404(Product, product_id)


    existing_item = BuildItem.query.filter_by(
        build_id=build.id,
        product_id=product.id
    ).first()


    if existing_item:

        flash("This component is already in the build.", "warning")
        return redirect(
            url_for(
                "main.build",
                build_id=build.id
            )
        )

    if product.stock <= 0:
        flash("This component is out of stock.", "error")
        return redirect(url_for("main.build", build_id=build.id))

    virtual_build = make_virtual_build(
        [item.product for item in build.items] + [product]
    )
    product_category = product.category.name
    issues = [
        result["message"]
        for result in check_build_compatibility(virtual_build)["results"]
        if result["compatible"] is False
        and product_category in result.get("pair", ())
    ]
    if issues:
        flash("This component is incompatible with the current build.", "error")
        return redirect(url_for("main.build", build_id=build.id))

    new_item = BuildItem(
        build_id=build.id,
        product_id=product.id
    )


    db.session.add(
        new_item
    )

    db.session.commit()


    return redirect(
        url_for(
            "main.build",
            build_id=build.id
        )
    )

# ================= PC RECOMMENDATION =================

@main.route("/recommendation", methods=["GET", "POST"])
def recommendation():

    recommendation_result = None
    analysis = None
    build_score = None
    missing_categories = []

    if request.method == "POST":

        usage = request.form.get("usage")
        budget = request.form.get("budget", type=float)

        if not usage or not budget or budget <= 0:

            recommendation_result = {
                "success": False,
                "message": "Please select a usage and enter a valid budget."
            }

        else:

            recommendation_result = recommend_components(
                usage,
                budget
            )

    if recommendation_result and recommendation_result.get("success"):

        picked = recommendation_result["recommendations"]

        if picked:

            analysis = analyze_products(
                list(picked.values())
            )

            build_score = calculate_build_score(
                picked,
                analysis["compatibility"],
                analysis["power"]
            )

        missing_categories = [
            category
            for category in USAGE_PROFILES[
                recommendation_result["usage"]
            ]
            if category not in picked
        ]

    return render_template(
        "recommendation.html",
        recommendation_result=recommendation_result,
        analysis=analysis,
        build_score=build_score,
        missing_categories=missing_categories
    )


# ================= CREATE BUILD FROM RECOMMENDATION =================

@main.route("/recommendation/create-build", methods=["POST"])
@login_required
def create_build_from_recommendation():

    usage = request.form.get("usage")
    budget = request.form.get("budget", type=float)

    if not usage or not budget or budget <= 0:
        flash("Please choose a usage and budget first.", "error")
        return redirect(url_for("main.recommendation"))

    # Recompute on the server instead of trusting product ids from the browser
    result = recommend_components(usage, budget)

    if not result["success"] or not result["recommendations"]:
        flash("We couldn't recommend any components for that budget.", "error")
        return redirect(url_for("main.recommendation"))

    new_build = Build(
        name=f"{USAGE_LABELS[result['usage']]} PC - ₹{budget:,.0f}",
        user_id=current_user.id
    )

    db.session.add(new_build)
    db.session.flush()

    for product in result["recommendations"].values():
        db.session.add(
            BuildItem(build_id=new_build.id, product_id=product.id)
        )

    db.session.commit()

    flash(
        "Build created from your recommendation. "
        "You can swap or remove any component below.",
        "success"
    )

    return redirect(url_for("main.build", build_id=new_build.id))


# ================= SWAP A COMPONENT =================

def _get_owned_build_item(build_id, item_id):

    build = db.get_or_404(Build, build_id)

    if build.user_id != current_user.id:
        abort(403)

    item = db.get_or_404(BuildItem, item_id)

    if item.build_id != build.id:
        abort(404)

    return build, item


@main.route("/build/<int:build_id>/swap/<int:item_id>")
@login_required
def swap_component(build_id, item_id):

    build, item = _get_owned_build_item(build_id, item_id)

    candidates = (
        Product.query
        .filter(
            Product.category_id == item.product.category_id,
            Product.id != item.product_id,
            Product.stock > 0
        )
        .order_by(Product.price.asc())
        .all()
    )

    return render_template(
        "swap.html",
        build=build,
        item=item,
        options=swap_options(build, item, candidates)
    )


@main.route(
    "/build/<int:build_id>/swap/<int:item_id>/<int:product_id>",
    methods=["POST"]
)
@login_required
def apply_swap(build_id, item_id, product_id):

    build, item = _get_owned_build_item(build_id, item_id)

    new_product = db.get_or_404(Product, product_id)

    # Only same-category, in-stock replacements are allowed
    if (
        new_product.category_id != item.product.category_id
        or new_product.stock <= 0
    ):
        abort(400)

    if any(other.product_id == new_product.id for other in build.items):
        flash(f"{new_product.name} is already in this build.", "warning")
        return redirect(url_for("main.build", build_id=build.id))

    old_name = item.product.name
    old_product = item.product
    category = old_product.category.name
    item.product = new_product

    issues = [
        r["message"]
        for r in check_build_compatibility(build)["results"]
        if r["compatible"] is False
        and category in r.get("pair", ())
    ]

    if issues:
        item.product = old_product
        flash(
            f"Cannot swap {old_name} for {new_product.name}: "
            "the replacement is incompatible.",
            "error"
        )
        return redirect(url_for("main.build", build_id=build.id))

    db.session.commit()
    flash(f"Swapped {old_name} for {new_product.name}.", "success")

    return redirect(url_for("main.build", build_id=build.id))