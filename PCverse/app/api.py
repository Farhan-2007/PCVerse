from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user, login_user,logout_user
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from app.models import Product, Category, Build, User,BuildItem
from app import db

from app.compatibility import check_build_compatibility
from app.performance import check_cpu_gpu_performance
from app.power_calculator import calculate_build_power
from app.usage_recommendation import get_usage_recommendation
from app.upgrade_suggestions import get_upgrade_suggestions
from app.build_tools import swap_options
from app.recommendation import recommend_components

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/products")
def products():
    products = (
        Product.query
        .order_by(Product.name.asc())
        .all()
    )


    return jsonify([
        {
            "id": product.id,
            "name": product.name,
            "brand": product.brand,
            "price": product.price,
            "stock": product.stock,
            "category_id": product.category_id,
            "image_file": product.image_file,
        }
        for product in products
    ])


@api.route("/categories")
def categories():
    categories = (
        Category.query
        .order_by(Category.name.asc())
        .all()
    )

    return jsonify([
        {
            "id": category.id,
            "name": category.name
        }
        for category in categories
    ])

@api.route("/builds")
@login_required
def builds():

    builds = (
        Build.query
        .filter_by(user_id=current_user.id)
        .order_by(Build.created_at.desc())
        .all()
    )

    return jsonify([
        {
            "id": build.id,
            "name": build.name,
            "created_at": build.created_at.isoformat(),
            "items": [
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "product_name": item.product.name
                }
                for item in build.items
            ]
        }
        for build in builds
    ])

@api.route("/products/<int:product_id>")
def product_detail(product_id):

    product = Product.query.get_or_404(product_id)

    return jsonify({
        "id": product.id,
        "name": product.name,
        "brand": product.brand,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
        "image_file": product.image_file,
        "specification": product.specification,
        "category_id": product.category_id
    })

@api.route("/me")
def me():

    if current_user.is_authenticated:
        return jsonify({
            "authenticated": True,
            "username": current_user.username
        })

    return jsonify({
        "authenticated": False
    })

@api.route("/login", methods=["POST"])
def login_api():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required."
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401

    login_user(user)

    return jsonify({
        "success": True,
        "username": user.username
    })

@api.route("/logout", methods=["POST"])
@login_required
def logout_api():

    logout_user()

    return jsonify({
        "success": True
    })

@api.route("/signup", methods=["POST"])
def signup_api():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({
            "success": False,
            "message": "All fields are required."
        }), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "success": False,
            "message": "An account with this email already exists."
        }), 409

    existing_username = User.query.filter_by(username=username).first()

    if existing_username:
        return jsonify({
            "success": False,
            "message": "This username is already taken."
        }), 409

    user = User(
        username=username,
        email=email,
        password=generate_password_hash(password)
    )

    db.session.add(user)
    db.session.commit()

    login_user(user)

    return jsonify({
        "success": True,
        "message": "Account created successfully."
    }), 201

def serialize_product(product):

    return {
        "id": product.id,
        "name": product.name,
        "brand": product.brand,
        "price": product.price,
        "image_file": product.image_file
    }

def make_json_safe(value):

    if isinstance(value, Product):
        return serialize_product(value)

    if isinstance(value, dict):
        return {
            key: make_json_safe(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            make_json_safe(item)
            for item in value
        ]

    if isinstance(value, tuple):
        return [
            make_json_safe(item)
            for item in value
        ]

    return value

@api.route("/builds/<int:build_id>")
@login_required
def build_detail(build_id):

    build = Build.query.get_or_404(build_id)

    if build.user_id != current_user.id:
        return jsonify({
            "success": False,
            "message": "Build not found."
        }), 404

    # -----------------------------
    # DUPLICATE COMPONENT CHECK
    # -----------------------------

    warnings = {}

    for item in build.items:

        category = item.product.category.name

        if category not in warnings:
            warnings[category] = []

        warnings[category].append(item)

    duplicate_warnings = {}

    for category, items in warnings.items():

        if len(items) > 1:
            duplicate_warnings[category] = [
                item.product.name
                for item in items
            ]

    # -----------------------------
    # COMPATIBILITY
    # -----------------------------

    compatibility_result = check_build_compatibility(build)

    # -----------------------------
    # CPU + GPU PERFORMANCE
    # -----------------------------

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

        performance_result = check_cpu_gpu_performance(
            cpu,
            gpu
        )

    # -----------------------------
    # POWER
    # -----------------------------

    power_result = calculate_build_power(build)

    # -----------------------------
    # TOTAL PRICE
    # -----------------------------

    total_price = 0

    for item in build.items:
        total_price += item.product.price

    # -----------------------------
    # UPGRADE SUGGESTIONS
    # -----------------------------

    upgrade_suggestions = get_upgrade_suggestions(build)

    # -----------------------------
    # RESPONSE
    # -----------------------------

    return jsonify(
    make_json_safe({
        "id": build.id,
        "name": build.name,
        "created_at": build.created_at.isoformat(),

        "items": [
            {
                "id": item.id,
                "product_id": item.product_id,
                "product_name": item.product.name,
                "category": item.product.category.name,
                "price": item.product.price,
                "image_file": item.product.image_file
            }
            for item in build.items
        ],

        "total_price": total_price,

        "duplicate_warnings": duplicate_warnings,

        "compatibility": compatibility_result,

        "performance": performance_result,

        "power": power_result,

        "upgrade_suggestions": upgrade_suggestions
    })
)

# ================= CREATE BUILD =================

@api.route("/builds", methods=["POST"])
@login_required
def create_build_api():

    data = request.get_json()

    build_name = data.get("name") if data else None

    if not build_name or not build_name.strip():
        return jsonify({
            "success": False,
            "message": "Build name is required."
        }), 400

    new_build = Build(
        name=build_name.strip(),
        user_id=current_user.id
    )

    db.session.add(new_build)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Build created successfully.",
        "build": {
            "id": new_build.id,
            "name": new_build.name
        }
    }), 201


# ================= DELETE BUILD =================

@api.route("/builds/<int:build_id>", methods=["DELETE"])
@login_required
def delete_build_api(build_id):

    build = Build.query.get_or_404(build_id)

    if build.user_id != current_user.id:
        return jsonify({
            "success": False,
            "message": "Build not found."
        }), 404

    db.session.delete(build)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Build deleted successfully."
    })


# ================= ADD COMPONENT =================

@api.route(
    "/builds/<int:build_id>/items/<int:product_id>",
    methods=["POST"]
)
@login_required
def add_component_api(build_id, product_id):

    build = Build.query.get_or_404(build_id)

    if build.user_id != current_user.id:
        return jsonify({
            "success": False,
            "message": "Build not found."
        }), 404

    product = Product.query.get_or_404(product_id)

    existing_item = BuildItem.query.filter_by(
        build_id=build.id,
        product_id=product.id
    ).first()

    if existing_item:
        return jsonify({
            "success": False,
            "message": "This component is already in the build."
        }), 400

    new_item = BuildItem(
        build_id=build.id,
        product_id=product.id
    )

    db.session.add(new_item)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Component added successfully."
    })


# ================= REMOVE COMPONENT =================

@api.route(
    "/builds/<int:build_id>/items/<int:item_id>",
    methods=["DELETE"]
)
@login_required
def remove_component_api(build_id, item_id):

    build = Build.query.get_or_404(build_id)

    if build.user_id != current_user.id:
        return jsonify({
            "success": False,
            "message": "Build not found."
        }), 404

    item = BuildItem.query.get_or_404(item_id)

    if item.build_id != build.id:
        return jsonify({
            "success": False,
            "message": "Component not found."
        }), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Component removed successfully."
    })

# ================= SWAP COMPONENT OPTIONS =================

@api.route(
    "/builds/<int:build_id>/items/<int:item_id>/swap-options",
    methods=["GET"]
)
@login_required
def swap_component_options_api(build_id, item_id):

    build = Build.query.get_or_404(build_id)

    if build.user_id != current_user.id:
        return jsonify({
            "success": False,
            "message": "Build not found."
        }), 404

    item = BuildItem.query.get_or_404(item_id)

    if item.build_id != build.id:
        return jsonify({
            "success": False,
            "message": "Component not found."
        }), 404

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

    options = swap_options(
        build,
        item,
        candidates
    )

    return jsonify({
        "success": True,
        "options": make_json_safe(options)
    })

@api.route(
    "/builds/<int:build_id>/items/<int:item_id>/swap/<int:product_id>",
    methods=["POST"]
)
@login_required
def apply_swap_api(build_id, item_id, product_id):

    build = Build.query.get_or_404(build_id)

    if build.user_id != current_user.id:
        return jsonify({
            "success": False,
            "message": "Build not found."
        }), 404

    item = BuildItem.query.get_or_404(item_id)

    if item.build_id != build.id:
        return jsonify({
            "success": False,
            "message": "Component not found."
        }), 404

    new_product = Product.query.get_or_404(product_id)

    if new_product.category_id != item.product.category_id:
        return jsonify({
            "success": False,
            "message": "Invalid replacement component."
        }), 400

    if new_product.stock <= 0:
        return jsonify({
            "success": False,
            "message": "This component is out of stock."
        }), 400

    if any(
        other.product_id == new_product.id
        for other in build.items
        if other.id != item.id
    ):
        return jsonify({
            "success": False,
            "message": "This component is already in the build."
        }), 400

    old_name = item.product.name

    item.product_id = new_product.id

    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Swapped {old_name} for {new_product.name}.",
        "build_id": build.id
    })

@api.route("/recommendation", methods=["POST"])
def recommendation_api():

    data = request.get_json() or {}

    usage = data.get("usage")
    budget = data.get("budget")

    if not usage:
        return jsonify({
            "success": False,
            "message": "Usage is required."
        }), 400

    try:
        budget = float(budget)
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "Budget must be a valid number."
        }), 400

    result = recommend_components(usage, budget)

    return jsonify(
        make_json_safe(result)
    )