from app.performance import check_cpu_gpu_performance


def calculate_build_score(
    recommendations,
    compatibility,
    power
):
    score = 0
    breakdown = {}

    # 1. Compatibility — 40 points
    if compatibility.get("compatible"):
        compatibility_score = 40
    else:
        compatibility_score = 0

    score += compatibility_score
    breakdown["Compatibility"] = compatibility_score

    # 2. CPU/GPU Balance — 30 points
    performance_result = check_cpu_gpu_performance(
    recommendations.get("CPU"),
    recommendations.get("GPU")
)

    if performance_result["status"] == "balanced":
        performance_score = 30
    elif performance_result["status"] in [
        "cpu_limited",
        "gpu_limited"
    ]:
        performance_score = 20
    else:
        performance_score = 10

    score += performance_score
    breakdown["CPU/GPU Balance"] = performance_score

    # 3. Power — 20 points
    if power.get("psu_compatible"):
        power_score = 20
    elif power.get("selected_psu"):
        power_score = 10
    else:
        power_score = 0

    score += power_score
    breakdown["Power"] = power_score

    # 4. Build completeness — 10 points
    required_categories = [
        "CPU",
        "GPU",
        "Motherboard",
        "RAM",
        "SSD",
        "Power Supply",
        "CPU Cooler",
        "Cabinet"
    ]

    required_categories = [
    "CPU",
    "GPU",
    "Motherboard",
    "RAM",
    "SSD",
    "Power Supply",
    "CPU Cooler",
    "Cabinet"
]

    if all(
        recommendations.get(category)
        for category in required_categories
    ):
        completeness_score = 10
    else:
        completeness_score = 0

    score += completeness_score
    breakdown["Build Completeness"] = completeness_score

    return {
        "score": score,
        "breakdown": breakdown,
        "performance": performance_result
    }