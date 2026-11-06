from types import SimpleNamespace

from app.compatibility import check_build_compatibility
from app.power_calculator import calculate_build_power


USAGE_LABELS = {
    "gaming": "Gaming",
    "programming": "Programming",
    "editing": "Video Editing",
    "3d": "3D / Rendering",
    "general": "General Use",
}


def make_virtual_build(products):
    """Wrap a list of products so the existing checkers can read it like a Build."""
    return SimpleNamespace(
        items=[SimpleNamespace(id=None, product=product) for product in products]
    )


def analyze_products(products):
    """Compatibility, power and price summary for a list of products."""
    build = make_virtual_build(products)

    return {
        "compatibility": check_build_compatibility(build),
        "power": calculate_build_power(build),
        "total_price": sum(product.price for product in products),
    }


def swap_options(build, item, candidates):
    """
    Describe what happens if `item` is replaced by each candidate product.
    Only compatibility results involving the swapped category count against
    a candidate, so problems elsewhere don't make every option look broken.
    """
    category = item.product.category.name

    other_products = [
        other.product for other in build.items if other.id != item.id
    ]
    current_power = calculate_build_power(build)

    options = []

    for candidate in candidates:

        virtual = make_virtual_build(other_products + [candidate])
        compatibility = check_build_compatibility(virtual)

        issues = [
            result["message"]
            for result in compatibility["results"]
            if result["compatible"] is False
            and category in result.get("pair", ())
        ]
        unknown_checks = [
            result["message"]
            for result in compatibility["results"]
            if result["compatible"] is None
            and category in result.get("pair", ())
        ]

        power = calculate_build_power(virtual)

        power_ok = (
            power["selected_psu"] is None
            or power["psu_compatible"]
            or (
                current_power["selected_psu"] is not None
                and not current_power["psu_compatible"]
                and power["recommended_psu"]
                <= current_power["recommended_psu"]
            )
        )

        options.append({
            "product": candidate,
            "price_difference": candidate.price - item.product.price,
            "compatible": not issues,
            "verification": "unknown" if unknown_checks else "verified",
            "issues": issues,
            "unknown_checks": unknown_checks,
            "power_ok": power_ok,
            "total_power": power["total_power"],
        })

    options.sort(
        key=lambda o: (not o["compatible"], not o["power_ok"], o["product"].price)
    )

    return options