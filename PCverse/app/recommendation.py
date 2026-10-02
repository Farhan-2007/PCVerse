from app import db
from app.models import Product
from app.specification_parser import parse_specification


USAGE_PROFILES = {
    "gaming": {
        "CPU": 0.25,
        "GPU": 0.40,
        "Motherboard": 0.10,
        "RAM": 0.08,
        "SSD": 0.07,
        "Power Supply": 0.05,
        "CPU Cooler": 0.03,
        "Cabinet": 0.02
    },

    "programming": {
        "CPU": 0.30,
        "GPU": 0.10,
        "Motherboard": 0.15,
        "RAM": 0.20,
        "SSD": 0.15,
        "Power Supply": 0.05,
        "CPU Cooler": 0.03,
        "Cabinet": 0.02
    },

    "editing": {
        "CPU": 0.30,
        "GPU": 0.25,
        "Motherboard": 0.10,
        "RAM": 0.15,
        "SSD": 0.10,
        "Power Supply": 0.05,
        "CPU Cooler": 0.03,
        "Cabinet": 0.02
    },

    "3d": {
        "CPU": 0.25,
        "GPU": 0.35,
        "Motherboard": 0.10,
        "RAM": 0.12,
        "SSD": 0.08,
        "Power Supply": 0.05,
        "CPU Cooler": 0.03,
        "Cabinet": 0.02
    },

    "general": {
        "CPU": 0.25,
        "GPU": 0.05,
        "Motherboard": 0.15,
        "RAM": 0.20,
        "SSD": 0.20,
        "Power Supply": 0.07,
        "CPU Cooler": 0.05,
        "Cabinet": 0.03
    }
}


def get_numeric_spec(product, keys):

    if not product or not product.specification:
        return 0

    specs = parse_specification(product.specification)

    for key in keys:

        value = specs.get(key)

        if not value:
            continue

        try:
            value = (
                value.replace("W", "")
                .replace("GB", "")
                .replace("GHz", "")
                .replace("MHz", "")
                .replace(",", "")
                .strip()
            )

            return float(value)

        except (ValueError, AttributeError):
            continue

    return 0


def get_product_performance(product):

    category = product.category.name

    if category == "CPU":

        cores = get_numeric_spec(
            product,
            ["Cores", "Core Count"]
        )

        boost = get_numeric_spec(
            product,
            ["Boost Clock", "Max Boost Clock"]
        )

        return cores * 10 + boost * 20

    if category == "GPU":

        memory = get_numeric_spec(
            product,
            ["Memory", "VRAM", "Memory Size"]
        )

        boost = get_numeric_spec(
            product,
            ["Boost Clock", "GPU Boost Clock"]
        )

        return memory * 10 + boost

    if category == "RAM":

        capacity = get_numeric_spec(
            product,
            ["Capacity", "Memory"]
        )

        speed = get_numeric_spec(
            product,
            ["Speed", "Memory Speed"]
        )

        return capacity * 10 + speed

    if category == "SSD":

        capacity = get_numeric_spec(
            product,
            ["Capacity", "Storage"]
        )

        return capacity

    return 0


def pick_best_product(products):
    """Highest score = performance + a bonus for performance per rupee."""

    best_product = None
    best_score = None

    for product in products:

        performance = get_product_performance(product)

        price_ratio = (
            performance / product.price
            if product.price > 0
            else 0
        )

        score = performance + (price_ratio * 100000)

        if best_score is None or score > best_score:
            best_product = product
            best_score = score

    return best_product


def choose_components(profile, optional, available, budget):
    """
    Decide which product to pick for each category.

    profile   : {"CPU": 0.25, "GPU": 0.40, ...}   budget share per category
    optional  : categories that may be left out
    available : {"CPU": [products in stock], ...}
    budget    : total money in rupees

    Returns (picked, minimum_budget).
    """

    # ---- Step 1: cheapest possible price in each category ----
    cheapest = {}

    for category, products in available.items():
        if products:
            cheapest[category] = min(p.price for p in products)

    minimum_budget = sum(
        price for category, price in cheapest.items()
        if category not in optional
    )

    if budget < minimum_budget:
        return {}, minimum_budget

    # ---- Step 2: go category by category ----
    picked = {}
    remaining = budget
    percent_left = sum(profile.values())

    categories = list(profile)

    for index, category in enumerate(categories):

        percentage = profile[category]

        # This category's share of the money that is STILL unspent.
        # Because 'remaining' shrinks only by what we really spend,
        # any unused money flows on to the next categories.
        share = remaining * percentage / percent_left
        percent_left -= percentage

        if category not in cheapest:
            continue   # nothing in stock for this category

        # Always keep enough money for the required parts that come later
        reserved = sum(
            cheapest[later]
            for later in categories[index + 1:]
            if later in cheapest and later not in optional
        )

        spend_limit = remaining - reserved

        if category in optional:
            limit = min(share, spend_limit)
        else:
            # Required part: allowed to cost a bit more than its share
            # if even the cheapest option is above the share.
            limit = min(max(share, cheapest[category]), spend_limit)

        affordable = [
            product for product in available[category]
            if product.price <= limit
        ]

        if not affordable:
            continue

        best_product = pick_best_product(affordable)

        picked[category] = best_product
        remaining -= best_product.price

    return picked, minimum_budget


def recommend_components(usage, budget):

    usage = usage.lower().strip()

    if usage not in USAGE_PROFILES:

        return {
            "success": False,
            "message": "Invalid usage selected.",
            "recommendations": {}
        }

    if budget <= 0:

        return {
            "success": False,
            "message": "Budget must be greater than zero.",
            "recommendations": {}
        }

    profile = USAGE_PROFILES[usage]
    optional = OPTIONAL_CATEGORIES.get(usage, [])

    # Database part: fetch in-stock products for every category
    available = {}

    for category in profile:

        available[category] = Product.query.filter(
            Product.category.has(name=category),
            Product.stock > 0
        ).all()

    # Decision part: no database needed
    recommendations, minimum_budget = choose_components(
        profile,
        optional,
        available,
        budget
    )

    if not recommendations:

        return {
            "success": False,
            "message": (
                f"This budget is too low for a complete {usage} PC. "
                f"The cheapest complete build we can recommend costs "
                f"about ₹{minimum_budget:,.0f}."
            ),
            "minimum_budget": minimum_budget,
            "recommendations": {}
        }

    total_estimated_price = sum(
        product.price for product in recommendations.values()
    )

    return {
        "success": True,
        "usage": usage,
        "budget": budget,
        "minimum_budget": minimum_budget,
        "total_estimated_price": total_estimated_price,
        "remaining_budget": budget - total_estimated_price,
        "recommendations": recommendations
    }