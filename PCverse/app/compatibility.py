from app.specification_parser import parse_specification


# =========================================================
# CPU ↔ MOTHERBOARD
# =========================================================

def check_cpu_motherboard(cpu, motherboard):

    cpu_specs = parse_specification(cpu.specification)
    motherboard_specs = parse_specification(motherboard.specification)

    cpu_socket = cpu_specs.get("Socket")
    motherboard_socket = motherboard_specs.get("Socket")

    if not cpu_socket or not motherboard_socket:

        return {
            "compatible": False,
            "message": "CPU or motherboard socket specification is missing."
        }

    if cpu_socket == motherboard_socket:

        return {
            "compatible": True,
            "message": (
                f"{cpu.name} and {motherboard.name} are compatible. "
                f"Both use {cpu_socket}."
            )
        }

    return {
        "compatible": False,
        "message": (
            f"{cpu.name} uses {cpu_socket}, "
            f"but {motherboard.name} uses {motherboard_socket}."
        )
    }


# =========================================================
# MOTHERBOARD ↔ RAM
# =========================================================

def check_motherboard_ram(motherboard, ram):

    motherboard_specs = parse_specification(motherboard.specification)
    ram_specs = parse_specification(ram.specification)

    motherboard_ram_type = motherboard_specs.get("RAM Type")
    ram_type = ram_specs.get("Type")

    if not motherboard_ram_type or not ram_type:

        return {
            "compatible": False,
            "message": "Motherboard or RAM type specification is missing."
        }

    if motherboard_ram_type == ram_type:

        return {
            "compatible": True,
            "message": (
                f"Motherboard and RAM are compatible. "
                f"Both use {ram_type}."
            )
        }

    return {
        "compatible": False,
        "message": (
            f"Motherboard supports {motherboard_ram_type}, "
            f"but the selected RAM is {ram_type}."
        )
    }


# =========================================================
# CPU ↔ CPU COOLER
# =========================================================

def check_cpu_cooler(cpu, cooler):

    cpu_specs = parse_specification(cpu.specification)
    cooler_specs = parse_specification(cooler.specification)

    cpu_socket = cpu_specs.get("Socket")
    cooler_sockets = cooler_specs.get("Socket Support")

    if not cpu_socket or not cooler_sockets:

        return {
            "compatible": False,
            "message": "CPU or cooler socket specification is missing."
        }

    supported_sockets = [
        socket.strip()
        for socket in cooler_sockets.split(",")
    ]

    if cpu_socket in supported_sockets:

        return {
            "compatible": True,
            "message": (
                f"{cpu.name} and {cooler.name} are compatible. "
                f"The cooler supports {cpu_socket}."
            )
        }

    return {
        "compatible": False,
        "message": (
            f"{cooler.name} does not support the CPU socket "
            f"{cpu_socket}."
        )
    }


# =========================================================
# GPU ↔ PSU
# =========================================================

def check_gpu_psu(gpu, psu):

    gpu_specs = parse_specification(gpu.specification)
    psu_specs = parse_specification(psu.specification)

    gpu_power = gpu_specs.get("Power Consumption")
    psu_wattage = psu_specs.get("Wattage")

    if not gpu_power or not psu_wattage:

        return {
            "compatible": False,
            "message": "GPU or PSU wattage specification is missing."
        }

    try:

        gpu_power = int(
            gpu_power.replace("W", "").strip()
        )

        psu_wattage = int(
            psu_wattage.replace("W", "").strip()
        )

    except ValueError:

        return {
            "compatible": False,
            "message": "Invalid GPU or PSU power specification."
        }

    # Extra power headroom
    required_power = gpu_power + 150

    if psu_wattage >= required_power:

        return {
            "compatible": True,
            "message": (
                f"{gpu.name} and {psu.name} have sufficient power. "
                f"GPU consumption: {gpu_power}W, "
                f"PSU: {psu_wattage}W."
            )
        }

    return {
        "compatible": False,
        "message": (
            f"{gpu.name} requires approximately {required_power}W "
            f"including headroom, but the selected PSU provides "
            f"only {psu_wattage}W."
        )
    }


# =========================================================
# GPU ↔ MOTHERBOARD
# =========================================================

def check_gpu_motherboard(gpu, motherboard):

    gpu_specs = parse_specification(gpu.specification)
    motherboard_specs = parse_specification(motherboard.specification)

    gpu_interface = gpu_specs.get("Interface")
    motherboard_pcie = motherboard_specs.get("PCIe Version")

    if not gpu_interface or not motherboard_pcie:

        return {
            "compatible": False,
            "message": (
                "GPU or motherboard PCIe specification is missing."
            )
        }

    # Extract PCIe generation numbers
    try:

        gpu_version = float(
            gpu_interface.replace("PCIe", "").strip()
        )

        motherboard_version = float(
            motherboard_pcie.replace("PCIe", "").strip()
        )

    except ValueError:

        return {
            "compatible": False,
            "message": "Invalid PCIe specification."
        }

    # PCIe is backward compatible.
    # A newer GPU can work with an older motherboard slot.
    if gpu_version >= motherboard_version:

        return {
            "compatible": True,
            "message": (
                f"{gpu.name} is compatible with "
                f"{motherboard.name}. "
                f"GPU: {gpu_interface}, "
                f"Motherboard: {motherboard_pcie}."
            )
        }

    return {
        "compatible": True,
        "message": (
            f"{gpu.name} is compatible with "
            f"{motherboard.name}. "
            f"GPU: {gpu_interface}, "
            f"Motherboard: {motherboard_pcie}. "
            f"The GPU will operate at the motherboard's PCIe generation."
        )
    }


# =========================================================
# GPU ↔ CABINET
# =========================================================

def check_gpu_cabinet(gpu, cabinet):

    gpu_specs = parse_specification(gpu.specification)
    cabinet_specs = parse_specification(cabinet.specification)

    gpu_length = gpu_specs.get("Length")
    gpu_clearance = cabinet_specs.get("GPU Clearance")

    if not gpu_length or not gpu_clearance:

        return {
            "compatible": False,
            "message": (
                "GPU length or cabinet GPU clearance "
                "specification is missing."
            )
        }

    try:

        gpu_length = float(
            gpu_length.replace("mm", "").strip()
        )

        gpu_clearance = float(
            gpu_clearance.replace("mm", "").strip()
        )

    except ValueError:

        return {
            "compatible": False,
            "message": "Invalid GPU length or cabinet clearance specification."
        }

    if gpu_length <= gpu_clearance:

        return {
            "compatible": True,
            "message": (
                f"{gpu.name} fits inside {cabinet.name}. "
                f"GPU length: {gpu_length} mm, "
                f"available clearance: {gpu_clearance} mm."
            )
        }

    return {
        "compatible": False,
        "message": (
            f"{gpu.name} is too long for {cabinet.name}. "
            f"GPU length: {gpu_length} mm, "
            f"available clearance: {gpu_clearance} mm."
        )
    }


# =========================================================
# COMPLETE BUILD COMPATIBILITY
# =========================================================

def check_build_compatibility(build):

    cpu = None
    motherboard = None
    ram = None
    gpu = None
    psu = None
    cooler = None
    cabinet = None

    # Find components in the build
    for item in build.items:

        category = item.product.category.name

        if category == "CPU":
            cpu = item.product

        elif category == "Motherboard":
            motherboard = item.product

        elif category == "RAM":
            ram = item.product

        elif category == "GPU":
            gpu = item.product

        elif category == "Power Supply":
            psu = item.product

        elif category == "CPU Cooler":
            cooler = item.product

        elif category == "Cabinet":
            cabinet = item.product


    # Store compatibility results
    results = []


    # CPU ↔ Motherboard
    if cpu and motherboard:

        results.append(
            check_cpu_motherboard(cpu, motherboard)
        )


    # Motherboard ↔ RAM
    if motherboard and ram:

        results.append(
            check_motherboard_ram(motherboard, ram)
        )


    # CPU ↔ Cooler
    if cpu and cooler:

        results.append(
            check_cpu_cooler(cpu, cooler)
        )


    # GPU ↔ PSU
    if gpu and psu:

        results.append(
            check_gpu_psu(gpu, psu)
        )


    # GPU ↔ Motherboard
    if gpu and motherboard:

        results.append(
            check_gpu_motherboard(gpu, motherboard)
        )


    # GPU ↔ Cabinet
    if gpu and cabinet:

        results.append(
            check_gpu_cabinet(gpu, cabinet)
        )


    # No checks possible
    if not results:

        return {
            "compatible": True,
            "message": "Add more components to check compatibility.",
            "results": []
        }


    # Check all results
    all_compatible = all(
        result["compatible"]
        for result in results
    )


    return {
        "compatible": all_compatible,

        "message": (
            "All checked components are compatible."
            if all_compatible
            else "One or more compatibility issues were detected."
        ),

        "results": results
    }