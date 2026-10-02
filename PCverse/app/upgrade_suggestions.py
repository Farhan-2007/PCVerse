from app import db
from app.models import Product
from app.recommendation import (
    get_product_performance,
    is_product_compatible
)


UPGRADE_CATEGORIES = [
    "CPU",
    "GPU",
    "RAM",
    "SSD"
]


def get_upgrade_suggestions(build):

    # Turn the current build into:
    # {"CPU": product, "GPU": product, ...}
    current_products = {}

    for item in build.items:
        category = item.product.category.name

        if category not in current_products:
            current_products[category] = item.product

    suggestions = []

    for category in UPGRADE_CATEGORIES:

        current_product = current_products.get(category)

        if not current_product:
            continue

        current_performance = get_product_performance(
            current_product
        )

        # We need a measurable performance value
        # to determine whether another product is an upgrade.
        if current_performance <= 0:
            continue

        candidates = (
            Product.query
            .filter(
                Product.category_id == current_product.category_id,
                Product.id != current_product.id,
                Product.stock > 0,
                Product.price > current_product.price
            )
            .all()
        )

        compatible_upgrades = []

        for candidate in candidates:

            candidate_performance = get_product_performance(
                candidate
            )

            if candidate_performance <= current_performance:
                continue

            selected_products = dict(current_products)

            # Pretend this candidate has replaced
            # the current component.
            selected_products[category] = candidate

            if not is_product_compatible(
                candidate,
                selected_products
            ):
                continue

            compatible_upgrades.append(
                (
                    candidate,
                    candidate_performance
                )
            )

        
        if not compatible_upgrades:
            continue

        # Pick the strongest compatible upgrade.
        best_product, best_performance = max(
            compatible_upgrades,
            key=lambda item: item[1]
        )

        build_item = next(
    (
        item
        for item in build.items
        if item.product_id == current_product.id
    ),
    None
)

        if not build_item:
            continue

        suggestions.append({
            "category": category,
            "current": current_product,
            "upgrade": best_product,
            "build_item_id": build_item.id,
            "current_price": current_product.price,
            "upgrade_price": best_product.price,
            "additional_cost": (
                best_product.price
                - current_product.price
            ),
            "performance_increase": (
                best_performance
                - current_performance
            )
        })

    return suggestions