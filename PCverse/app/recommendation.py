from app import db
from app.models import Product
from app.specification_parser import parse_specification

from app.compatibility import (
    check_cpu_motherboard,
    check_motherboard_ram,
    check_cpu_cooler,
    check_gpu_psu,
    check_gpu_motherboard,
    check_gpu_cabinet
)

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


OPTIONAL_CATEGORIES = {
    "gaming": [],
    "programming": [],
    "editing": [],
    "3d": [],
    "general": []
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
    """
    Select the product with the highest performance score.

    The score combines:
    - raw performance
    - performance per rupee
    """

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

def get_recommendation_reason(category, usage, product):
    reasons = {
        "gaming": {
            "CPU": "Chosen to provide strong gaming performance while keeping enough budget available for the GPU and other components.",
            "GPU": "Given the highest budget priority for gaming because the GPU has a major impact on gaming performance.",
            "Motherboard": "Selected to provide the required CPU socket and platform compatibility while staying within the build budget.",
            "RAM": "Selected to provide enough memory for modern gaming while maintaining a balanced overall build.",
            "SSD": "Selected to provide fast storage while keeping the overall build within budget.",
            "Power Supply": "Selected because its wattage is sufficient for the recommended components.",
            "CPU Cooler": "Selected to provide adequate CPU cooling while keeping the build balanced.",
            "Cabinet": "Selected because it supports the required motherboard form factor and provides sufficient GPU clearance."
        },
        "programming": {
            "CPU": "Given high priority because CPU performance is important for compiling code and running development workloads.",
            "GPU": "Given lower priority because programming workloads generally place more emphasis on CPU, RAM, and storage.",
            "Motherboard": "Selected to provide the required platform compatibility while staying within the build budget.",
            "RAM": "Given high priority because development tools, IDEs, browsers, and virtual environments can use significant memory.",
            "SSD": "Given high priority to provide fast storage for applications, projects, and development tools.",
            "Power Supply": "Selected because its wattage is sufficient for the recommended components.",
            "CPU Cooler": "Selected to provide adequate CPU cooling while keeping the build balanced.",
            "Cabinet": "Selected because it supports the required motherboard form factor and component clearance."
        },
        "editing": {
            "CPU": "Given high priority because CPU performance is important for many editing and rendering workloads.",
            "GPU": "Given high priority because GPU acceleration can improve performance in supported editing workloads.",
            "Motherboard": "Selected to provide the required platform compatibility while staying within the build budget.",
            "RAM": "Given high priority because editing applications can benefit from additional memory.",
            "SSD": "Selected to provide fast storage for applications and project files.",
            "Power Supply": "Selected because its wattage is sufficient for the recommended components.",
            "CPU Cooler": "Selected to provide adequate CPU cooling while keeping the build balanced.",
            "Cabinet": "Selected because it supports the required motherboard form factor and component clearance."
        },
        "3d": {
            "CPU": "Given high priority because CPU performance is important for 3D workloads and rendering.",
            "GPU": "Given high priority because GPU performance is important for many 3D applications and rendering workloads.",
            "Motherboard": "Selected to provide the required platform compatibility while staying within the build budget.",
            "RAM": "Given priority because 3D applications can benefit from additional memory.",
            "SSD": "Selected to provide fast storage for applications and project files.",
            "Power Supply": "Selected because its wattage is sufficient for the recommended components.",
            "CPU Cooler": "Selected to provide adequate CPU cooling while keeping the build balanced.",
            "Cabinet": "Selected because it supports the required motherboard form factor and component clearance."
        },
        "general": {
            "CPU": "Selected as a balanced processor for everyday workloads.",
            "GPU": "Kept at a lower budget priority because general workloads do not require a high-end dedicated GPU.",
            "Motherboard": "Selected to provide the required platform compatibility while staying within the build budget.",
            "RAM": "Given high priority because sufficient memory helps keep everyday multitasking responsive.",
            "SSD": "Given high priority because fast storage improves application and system responsiveness.",
            "Power Supply": "Selected because its wattage is sufficient for the recommended components.",
            "CPU Cooler": "Selected to provide adequate CPU cooling while keeping the build balanced.",
            "Cabinet": "Selected because it supports the required motherboard form factor and component clearance."
        }
    }

    return reasons.get(usage, {}).get(
        category,
        f"Selected as a suitable {category} for this build."
    )

def is_product_compatible(product, selected_products):
    """
    Check a candidate product against the components
    that have already been selected.
    """

    category = product.category.name

    cpu = selected_products.get("CPU")
    gpu = selected_products.get("GPU")
    motherboard = selected_products.get("Motherboard")
    ram = selected_products.get("RAM")
    psu = selected_products.get("Power Supply")
    cooler = selected_products.get("CPU Cooler")
    cabinet = selected_products.get("Cabinet")

    checks = []

    if category == "Motherboard" and cpu:
        checks.append(
            check_cpu_motherboard(cpu, product)
        )

    elif category == "RAM" and motherboard:
        checks.append(
            check_motherboard_ram(motherboard, product)
        )

    elif category == "CPU Cooler" and cpu:
        checks.append(
            check_cpu_cooler(cpu, product)
        )

    elif category == "Power Supply" and gpu:
        checks.append(
            check_gpu_psu(gpu, product)
        )

    elif category == "GPU":
        if motherboard:
            checks.append(
                check_gpu_motherboard(product, motherboard)
            )

        if psu:
            checks.append(
                check_gpu_psu(product, psu)
            )

        if cabinet:
            checks.append(
                check_gpu_cabinet(product, cabinet)
            )

    elif category == "Cabinet" and gpu:
        checks.append(
            check_gpu_cabinet(gpu, product)
        )

    return all(
        result["compatible"]
        for result in checks
    )

def upgrade_components(
    recommendations,
    available,
    remaining_budget,
    usage
):
    """
    Use leftover budget to upgrade important components.

    The upgrade priority depends on the user's usage.
    """

    priorities = {
        "gaming": [
            "GPU",
            "CPU",
            "RAM",
            "SSD"
        ],

        "programming": [
            "CPU",
            "RAM",
            "SSD",
            "GPU"
        ],

        "editing": [
            "CPU",
            "GPU",
            "RAM",
            "SSD"
        ],

        "3d": [
            "GPU",
            "CPU",
            "RAM",
            "SSD"
        ],

        "general": [
            "RAM",
            "SSD",
            "CPU",
            "GPU"
        ]
    }

    priority = priorities.get(
        usage,
        ["CPU", "GPU", "RAM", "SSD"]
    )

    upgraded = True

    while upgraded:

        upgraded = False

        for category in priority:

            current_product = recommendations.get(
                category
            )

            if not current_product:
                continue

            candidates = [
                product
                for product in available.get(
                    category,
                    []
                )
                if product.price > current_product.price
                and product.price - current_product.price
                <= remaining_budget
            ]

            if not candidates:
                continue

            current_performance = get_product_performance(
                current_product
            )

            best_upgrade = None
            best_upgrade_score = None

            for product in candidates:

                extra_cost = (
                    product.price
                    - current_product.price
                )

                new_performance = get_product_performance(
                    product
                )

                performance_gain = (
                    new_performance
                    - current_performance
                )

                if extra_cost <= 0:
                    continue

                upgrade_score = (
                    performance_gain / extra_cost
                )

                if (
                    best_upgrade_score is None
                    or upgrade_score > best_upgrade_score
                ):
                    best_upgrade = product
                    best_upgrade_score = upgrade_score

            if best_upgrade:

                extra_cost = (
                    best_upgrade.price
                    - current_product.price
                )

                recommendations[category] = (
                    best_upgrade
                )

                remaining_budget -= extra_cost

                upgraded = True

                break

    return recommendations, remaining_budget


def choose_components(profile, optional, available, budget):
    """
    Select the best available components while respecting the
    user's total budget and the usage profile.
    """

    # ---------------------------------------------------------
    # STEP 1: Find the cheapest product in every category
    # ---------------------------------------------------------

    cheapest = {}
    missing_required = []

    for category, products in available.items():

        if products:

            cheapest[category] = min(
                product.price
                for product in products
            )

        elif category not in optional:

            missing_required.append(category)

    # A required category has no products in stock.
    if missing_required:

        return {}, None

    # Calculate the cheapest possible complete PC.
    minimum_budget = sum(
        price
        for category, price in cheapest.items()
        if category not in optional
    )

    print("CHEAPEST PRODUCTS:")

    for category, price in cheapest.items():
        print(category, price)

    print("MINIMUM BUDGET:", minimum_budget)

    # The budget cannot build a complete PC.
    if budget < minimum_budget:

        return {}, minimum_budget

    # ---------------------------------------------------------
    # STEP 2: Select components
    # ---------------------------------------------------------

    picked = {}

    remaining = budget

    categories = list(profile)

    percent_left = sum(profile.values())

    print("AVAILABLE CPUS:")

    for cpu in available.get("CPU", []):    

        print(
            cpu.name,
            cpu.specification
        )

    print("AVAILABLE MOTHERBOARDS:")

    for motherboard in available.get("Motherboard", []):

        print(
            motherboard.name,
            motherboard.specification
        )

    for index, category in enumerate(categories):

        percentage = profile[category]

        # Calculate the category's target share
        # from the money still available.
        share = (
            remaining * percentage / percent_left
        )

        percent_left -= percentage

        # Safety check.
        if category not in available:
            continue

        if not available[category]:
            continue

        # Skip CPUs that have no compatible motherboard.
        if category == "CPU":
            compatible_cpus = []

            for cpu in available["CPU"]:

                print("TESTING CPU:", cpu.name)

                for motherboard in available.get("Motherboard", []):

                    result = check_cpu_motherboard(
                        cpu,
                        motherboard
                    )

                    print(
                        "  WITH MOTHERBOARD:",
                        motherboard.name,
                        "=>",
                        result
                    )

                    if result["compatible"]:
                        compatible_cpus.append(cpu)
                        break

            print(
                "COMPATIBLE CPUS:",
                [cpu.name for cpu in compatible_cpus]
            )

            if not compatible_cpus:
                return {}, minimum_budget

            available["CPU"] = compatible_cpus

        # -----------------------------------------------------
        # Reserve money for all required categories
        # that come after this one.
        # -----------------------------------------------------

        reserved = 0

        for later_category in categories[index + 1:]:

            if later_category in optional:
                continue

            if later_category in cheapest:

                reserved += cheapest[later_category]

        # Money that this category is allowed to use.
        spend_limit = remaining - reserved

        # The component must at least cost as much
        # as the cheapest available product.
        limit = max(
            share,
            cheapest[category]
        )

        # Never spend more than the money available
        # after reserving future components.
        limit = min(
            limit,
            spend_limit
        )

        # -----------------------------------------------------
        # Find products within the allowed price.
        # -----------------------------------------------------

        affordable = [
            product
            for product in available[category]
            if (
                product.price <= limit
                and is_product_compatible(
                    product,
                    picked
                )
            )
        ]

        # -----------------------------------------------------
        # If products fit, choose the best one.
        # -----------------------------------------------------

        if affordable:

            best_product = pick_best_product(affordable)

            picked[category] = best_product
            remaining -= best_product.price

            print(
                "SELECTED:",
                category,
                best_product.name,
                best_product.price
            )

        else:

            print(
                "NO PRODUCT FOR:",
                category,
                "SPEND LIMIT:",
                spend_limit
            )

            compatible_products = [
                product
                for product in available[category]
                if (
                    product.price <= spend_limit
                    and is_product_compatible(
                        product,
                        picked
                    )
                )
            ]

            if compatible_products:

                cheapest_product = min(
                    compatible_products,
                    key=lambda product: product.price
                )

                picked[category] = cheapest_product
                remaining -= cheapest_product.price

            else:

                print(
                    "FAILED:",
                    category
                )

                return picked, minimum_budget

    return picked, minimum_budget

        # Pick the best product from the affordable options.

def recommend_components(usage, budget):

    usage = usage.lower().strip()

    # ---------------------------------------------------------
    # Validate usage
    # ---------------------------------------------------------

    if usage not in USAGE_PROFILES:

        return {
            "success": False,
            "message": "Invalid usage selected.",
            "recommendations": {}
        }

    # ---------------------------------------------------------
    # Validate budget
    # ---------------------------------------------------------

    if budget <= 0:

        return {
            "success": False,
            "message": "Budget must be greater than zero.",
            "recommendations": {}
        }

    profile = USAGE_PROFILES[usage]

    optional = OPTIONAL_CATEGORIES.get(
        usage,
        []
    )

    # ---------------------------------------------------------
    # Get available products from database
    # ---------------------------------------------------------

    available = {}

    for category in profile:

        available[category] = Product.query.filter(
            Product.category.has(name=category),
            Product.stock > 0
        ).all()

    # ---------------------------------------------------------
    # Choose components
    # ---------------------------------------------------------

    recommendations, minimum_budget = choose_components(
        profile,
        optional,
        available,
        budget
    )

    # ---------------------------------------------------------
    # Required category has no products
    # ---------------------------------------------------------

    if minimum_budget is None:

        missing_categories = [
            category
            for category, products in available.items()
            if not products
            and category not in optional
        ]

        return {
            "success": False,
            "message": (
                "A complete PC cannot be recommended because "
                "these required categories have no products in stock: "
                + ", ".join(missing_categories)
            ),
            "recommendations": {}
        }

    # ---------------------------------------------------------
    # Budget is too low
    # ---------------------------------------------------------

        # ---------------------------------------------------------
    # Budget is too low
    # ---------------------------------------------------------

    if budget < minimum_budget:

        shortfall = minimum_budget - budget

        return {
            "success": False,
            "message": (
                "A complete PC could not be built within this budget. "
                f"Minimum available budget: ₹{minimum_budget:,.0f}. "
                f"Your budget: ₹{budget:,.0f}. "
                f"You need approximately ₹{shortfall:,.0f} more."
            ),
            "minimum_budget": minimum_budget,
            "recommendations": {}
        }

    # ---------------------------------------------------------
    # Calculate final price
    # ---------------------------------------------------------

    total_estimated_price = sum(
        product.price
        for product in recommendations.values()
    )

    remaining_budget = (
        budget - total_estimated_price
    )

    recommendations, remaining_budget = upgrade_components(
    recommendations,
    available,
    remaining_budget,
    usage
)

    total_estimated_price = sum(
        product.price
        for product in recommendations.values()
)

    # ---------------------------------------------------------
    # Return successful recommendation
    # ---------------------------------------------------------

    reasons = {
    category: get_recommendation_reason(
        category,
        usage,
        product
    )
    for category, product in recommendations.items()
}

    return {
        "success": True,
        "usage": usage,
        "budget": budget,
        "minimum_budget": minimum_budget,
        "total_estimated_price": total_estimated_price,
        "remaining_budget": remaining_budget,
        "recommendations": recommendations,
        "reasons": reasons
    }