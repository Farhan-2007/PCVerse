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

    recommendations = {}

    total_estimated_price = 0

    for category, percentage in profile.items():

        category_budget = budget * percentage

        products = Product.query.join(
            Product.category
        ).filter(
            Product.category.has(name=category),
            Product.stock > 0,
            Product.price <= category_budget
        ).all()

        if not products:

            continue

        scored_products = []

        for product in products:

            performance = get_product_performance(product)

            price_ratio = (
                performance / product.price
                if product.price > 0
                else 0
            )

            score = performance + (price_ratio * 100000)

            scored_products.append(
                (product, score)
            )

        scored_products.sort(
            key=lambda x: x[1],
            reverse=True
        )

        best_product = scored_products[0][0]

        recommendations[category] = best_product

        total_estimated_price += best_product.price

    return {
        "success": True,
        "usage": usage,
        "budget": budget,
        "total_estimated_price": total_estimated_price,
        "remaining_budget": budget - total_estimated_price,
        "recommendations": recommendations
    }