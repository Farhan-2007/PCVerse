from app.specification_parser import parse_specification


def get_power(product):

    if not product or not product.specification:
        return 0

    specs = parse_specification(product.specification)

    power = specs.get("TDP")

    if not power:
        power = specs.get("Power Consumption")

    if not power:
        return 0

    return int(
        power.replace("W", "").strip()
    )


def calculate_build_power(build):

    total_power = 0
    selected_psu = None

    for item in build.items:

        product = item.product
        category = product.category.name

        total_power += get_power(product)

        if category == "Power Supply":
            selected_psu = product

    recommended_psu = total_power + 150

    psu_options = [550, 650, 750, 850, 1000, 1200]

    recommended_options = [
            wattage
            for wattage in psu_options
            if wattage >= recommended_psu
        ]

    psu_wattage = 0

    if selected_psu:

        specs = parse_specification(
            selected_psu.specification
        )

        wattage = specs.get("Wattage")

        if wattage:

            psu_wattage = int(
                wattage.replace("W", "").strip()
            )

    if selected_psu:

        if psu_wattage >= recommended_psu:

            psu_status = "PSU is sufficient."
            psu_compatible = True
            headroom = psu_wattage - total_power

        else:

            psu_status = "PSU may not provide enough power."
            psu_compatible = False
            headroom = psu_wattage - total_power

    else:

        psu_status = "No PSU selected yet."
        psu_compatible = False
        headroom = 0

    return {
        "total_power": total_power,
        "recommended_psu": recommended_psu,
        "recommended_options": recommended_options,
        "selected_psu": selected_psu,
        "psu_wattage": psu_wattage,
        "psu_status": psu_status,
        "psu_compatible": psu_compatible,
        "headroom": headroom
    }