import re

from app.specification_parser import parse_specification
from app.power_calculator import calculate_build_power


def _unknown(message):
    return {
        "compatible": None,
        "status": "unknown",
        "message": message
    }


def _result(compatible, message):
    return {
        "compatible": compatible,
        "status": "compatible" if compatible else "incompatible",
        "message": message
    }


# =========================================================
# CPU ↔ MOTHERBOARD
# =========================================================

def check_cpu_motherboard(cpu, motherboard):

    cpu_specs = parse_specification(cpu.specification)
    motherboard_specs = parse_specification(motherboard.specification)

    cpu_socket = cpu_specs.get("Socket")
    motherboard_socket = motherboard_specs.get("Socket")

    if not cpu_socket or not motherboard_socket:

        return _unknown("CPU or motherboard socket specification is missing.")

    if cpu_socket.strip().casefold() == motherboard_socket.strip().casefold():

        return _result(
            True,
            (
                f"{cpu.name} and {motherboard.name} are compatible. "
                f"Both use {cpu_socket}."
            )
        )

    return _result(
        False,
        (
            f"{cpu.name} uses {cpu_socket}, "
            f"but {motherboard.name} uses {motherboard_socket}."
        )
    )


# =========================================================
# MOTHERBOARD ↔ RAM
# =========================================================

def check_motherboard_ram(motherboard, ram):

    motherboard_specs = parse_specification(motherboard.specification)
    ram_specs = parse_specification(ram.specification)

    motherboard_ram_type = motherboard_specs.get("RAM Type")
    ram_type = ram_specs.get("Type")

    if not motherboard_ram_type or not ram_type:

        return _unknown("Motherboard or RAM type specification is missing.")

    if motherboard_ram_type.strip().casefold() == ram_type.strip().casefold():

        return _result(
            True,
            (
                f"Motherboard and RAM are compatible. "
                f"Both use {ram_type}."
            )
        )

    return _result(
        False,
        (
            f"Motherboard supports {motherboard_ram_type}, "
            f"but the selected RAM is {ram_type}."
        )
    )


# =========================================================
# CPU ↔ CPU COOLER
# =========================================================

def check_cpu_cooler(cpu, cooler):

    cpu_specs = parse_specification(cpu.specification)
    cooler_specs = parse_specification(cooler.specification)

    cpu_socket = cpu_specs.get("Socket")
    cooler_sockets = cooler_specs.get("Socket Support")

    if not cpu_socket or not cooler_sockets:

        return _unknown("CPU or cooler socket specification is missing.")

    supported_sockets = [
        socket.strip()
        for socket in cooler_sockets.split(",")
    ]

    if any(
        cpu_socket.strip().casefold() == socket.casefold()
        for socket in supported_sockets
    ):

        return _result(
            True,
            (
                f"{cpu.name} and {cooler.name} are compatible. "
                f"The cooler supports {cpu_socket}."
            )
        )

    return _result(
        False,
        (
            f"{cooler.name} does not support the CPU socket "
            f"{cpu_socket}."
        )
    )


# =========================================================
# GPU ↔ PSU
# =========================================================

def check_gpu_psu(gpu, psu, required_wattage=None):

    gpu_specs = parse_specification(gpu.specification)
    psu_specs = parse_specification(psu.specification)

    gpu_power = gpu_specs.get("Power Consumption")
    psu_wattage = psu_specs.get("Wattage")

    if not gpu_power or not psu_wattage:

        return _unknown("GPU or PSU wattage specification is missing.")

    gpu_match = re.search(r"\d+(?:\.\d+)?", gpu_power)
    psu_match = re.search(r"\d+(?:\.\d+)?", psu_wattage)
    if not gpu_match or not psu_match:
        return _unknown("Invalid GPU or PSU power specification.")

    gpu_power = int(float(gpu_match.group()))
    psu_wattage = int(float(psu_match.group()))
    required_power = required_wattage or gpu_power + 150

    if psu_wattage >= required_power:

        return _result(
            True,
            (
                f"{gpu.name} and {psu.name} have sufficient power. "
                f"Estimated system requirement: {required_power}W, "
                f"PSU: {psu_wattage}W."
            )
        )

    return _result(
        False,
        (
            f"The build requires approximately {required_power}W "
            f"including headroom, but {psu.name} provides only "
            f"{psu_wattage}W."
        )
    )


# =========================================================
# GPU ↔ MOTHERBOARD
# =========================================================

def check_gpu_motherboard(gpu, motherboard):

    gpu_specs = parse_specification(gpu.specification)
    motherboard_specs = parse_specification(motherboard.specification)

    gpu_interface = gpu_specs.get("Interface")
    motherboard_pcie = motherboard_specs.get("PCIe Version")

    if not gpu_interface or not motherboard_pcie:

        return _unknown(
            (
                "GPU or motherboard PCIe specification is missing."
            )
        )

    # Extract PCIe generation numbers
    gpu_match = re.search(
        r"PCIe\s*([0-9]+(?:\.[0-9]+)?)",
        gpu_interface,
        re.IGNORECASE
    )
    motherboard_match = re.search(
        r"PCIe\s*([0-9]+(?:\.[0-9]+)?)",
        motherboard_pcie,
        re.IGNORECASE
    )
    if not gpu_match or not motherboard_match:
        return _unknown("Invalid PCIe specification.")
    gpu_version = float(gpu_match.group(1))
    motherboard_version = float(motherboard_match.group(1))

    # PCIe is backward compatible.
    # A newer GPU can work with an older motherboard slot.
    return _result(
        True,
        (
            f"{gpu.name} is compatible with "
            f"{motherboard.name}. "
            f"GPU: {gpu_interface}, "
            f"Motherboard: {motherboard_pcie}. "
            + (
                "The GPU will operate at the motherboard's PCIe generation."
                if gpu_version > motherboard_version
                else "PCIe interface generations are compatible."
            )
        )
    )


# =========================================================
# GPU ↔ CABINET
# =========================================================

def check_gpu_cabinet(gpu, cabinet):

    gpu_specs = parse_specification(gpu.specification)
    cabinet_specs = parse_specification(cabinet.specification)

    gpu_length = gpu_specs.get("Length")
    gpu_clearance = cabinet_specs.get("GPU Clearance")

    if not gpu_length or not gpu_clearance:

        return _unknown(
            (
                "GPU length or cabinet GPU clearance "
                "specification is missing."
            )
        )

    gpu_match = re.search(r"\d+(?:\.\d+)?", gpu_length)
    clearance_match = re.search(r"\d+(?:\.\d+)?", gpu_clearance)
    if not gpu_match or not clearance_match:
        return _unknown("Invalid GPU length or cabinet clearance specification.")
    gpu_length = float(gpu_match.group())
    gpu_clearance = float(clearance_match.group())

    if gpu_length <= gpu_clearance:

        return _result(
            True,
            (
                f"{gpu.name} fits inside {cabinet.name}. "
                f"GPU length: {gpu_length} mm, "
                f"available clearance: {gpu_clearance} mm."
            )
        )

    return _result(
        False,
        (
            f"{gpu.name} is too long for {cabinet.name}. "
            f"GPU length: {gpu_length} mm, "
            f"available clearance: {gpu_clearance} mm."
        )
    )

def _tag(result, pair):
    """Attach the pair of categories a result refers to (used by swap)."""
    result["pair"] = pair
    return result

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
            _tag(
                check_cpu_motherboard(cpu, motherboard),
                ("CPU", "Motherboard")
            )
        )


    # Motherboard ↔ RAM
    if motherboard and ram:

        results.append(
            _tag(
                check_motherboard_ram(motherboard, ram),
                ("Motherboard", "RAM")
            )
        )


    # CPU ↔ Cooler
    if cpu and cooler:

        results.append(
            _tag(
                check_cpu_cooler(cpu, cooler),
                ("CPU", "CPU Cooler")
            )
        )


    # GPU ↔ PSU
    if gpu and psu:

        power = calculate_build_power(build)
        results.append(
            _tag(
                check_gpu_psu(
                    gpu,
                    psu,
                    power["recommended_psu"]
                ),
                ("GPU", "Power Supply")
            )
        )


    # GPU ↔ Motherboard
    if gpu and motherboard:

        results.append(
            _tag(
                check_gpu_motherboard(gpu, motherboard),
                ("GPU", "Motherboard")
            )
        )


    # GPU ↔ Cabinet
    if gpu and cabinet:

        results.append(
            _tag(
                check_gpu_cabinet(gpu, cabinet),
                ("GPU", "Cabinet")
            )
        )


    # No checks possible
    if not results:

        return {
            "compatible": None,
            "status": "unknown",
            "message": "Add more components to check compatibility.",
            "results": []
        }

    has_incompatibility = any(
        result["compatible"] is False
        for result in results
    )
    has_unknown = any(
        result["compatible"] is None
        for result in results
    )
    all_compatible = not has_incompatibility and not has_unknown


    return {
        "compatible": (
            False if has_incompatibility
            else None if has_unknown
            else True
        ),
        "status": (
            "incompatible" if has_incompatibility
            else "unknown" if has_unknown
            else "compatible"
        ),

        "message": (
            "All checked components are compatible."
            if all_compatible
            else (
                "One or more compatibility issues were detected."
                if has_incompatibility
                else "No incompatibilities were found, but some checks could not be verified."
            )
        ),

        "results": results
    }