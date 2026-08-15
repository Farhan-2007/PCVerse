from app.specification_parser import parse_specification


def get_specs(product):

    if not product or not product.specification:
        return {}

    return parse_specification(product.specification)


def get_cpu_score(cpu):

    specs = get_specs(cpu)

    cores = specs.get("Cores")
    boost_clock = specs.get("Boost Clock")

    if not cores or not boost_clock:
        return 0

    cores = int(cores)

    boost_clock = float(
        boost_clock.replace("GHz", "").strip()
    )

    return cores * boost_clock


def get_gpu_score(gpu):

    specs = get_specs(gpu)

    vram = specs.get("VRAM")
    boost_clock = specs.get("Boost Clock")

    if not vram or not boost_clock:
        return 0

    vram = int(
        vram.replace("GB", "").strip()
    )

    boost_clock = float(
        boost_clock.replace("GHz", "").strip()
    )

    return vram * boost_clock


def get_ram_capacity(ram):

    specs = get_specs(ram)

    capacity = specs.get("Capacity")

    if not capacity:
        return 0

    return int(
        capacity.replace("GB", "").strip()
    )


def get_build_components(build):

    cpu = None
    gpu = None
    ram = None

    for item in build.items:

        category = item.product.category.name

        if category == "CPU":
            cpu = item.product

        elif category == "GPU":
            gpu = item.product

        elif category == "RAM":
            ram = item.product

    return cpu, gpu, ram


def get_usage_recommendation(build, usage):

    cpu, gpu, ram = get_build_components(build)

    if not usage:

        return None

    cpu_score = get_cpu_score(cpu)
    gpu_score = get_gpu_score(gpu)
    ram_capacity = get_ram_capacity(ram)

    if usage == "gaming":

        if not cpu or not gpu:

            return {
                "usage": "Gaming",
                "status": "warning",
                "message": (
                    "Add both a CPU and GPU to get a gaming recommendation."
                )
            }

        if gpu_score >= 25 and cpu_score >= 35:

            message = (
                "Your build is well suited for gaming. "
                "It should provide a strong gaming experience."
            )

            status = "excellent"

        elif gpu_score >= 18 and cpu_score >= 25:

            message = (
                "Your build should handle gaming comfortably. "
                "The performance is suitable for mainstream gaming."
            )

            status = "good"

        else:

            message = (
                "Your build may be limited for demanding gaming. "
                "Consider upgrading the CPU or GPU."
            )

            status = "warning"

    elif usage == "programming":

        if not cpu:

            return {
                "usage": "Programming",
                "status": "warning",
                "message": "Add a CPU to get a programming recommendation."
            }

        if cpu_score >= 35 and ram_capacity >= 32:

            message = (
                "Your build is excellent for programming, "
                "development environments, virtual machines, "
                "and multitasking."
            )

            status = "excellent"

        elif cpu_score >= 25 and ram_capacity >= 16:

            message = (
                "Your build is suitable for programming "
                "and normal development workloads."
            )

            status = "good"

        else:

            message = (
                "Your build may struggle with heavy development workloads. "
                "Consider a stronger CPU or more RAM."
            )

            status = "warning"

    elif usage == "editing":

        if not cpu or not gpu or not ram:

            return {
                "usage": "Video Editing",
                "status": "warning",
                "message": (
                    "Add CPU, GPU and RAM to get a video editing recommendation."
                )
            }

        if cpu_score >= 35 and gpu_score >= 20 and ram_capacity >= 32:

            message = (
                "Your build is well suited for video editing "
                "and demanding creative workloads."
            )

            status = "excellent"

        elif cpu_score >= 25 and gpu_score >= 15 and ram_capacity >= 16:

            message = (
                "Your build should handle standard video editing workloads."
            )

            status = "good"

        else:

            message = (
                "Your build may struggle with demanding video editing. "
                "Consider upgrading the CPU, GPU or RAM."
            )

            status = "warning"

    elif usage == "3d":

        if not cpu or not gpu:

            return {
                "usage": "3D / Rendering",
                "status": "warning",
                "message": (
                    "Add both CPU and GPU to get a 3D/rendering recommendation."
                )
            }

        if cpu_score >= 35 and gpu_score >= 25:

            message = (
                "Your build is well suited for 3D rendering "
                "and demanding graphical workloads."
            )

            status = "excellent"

        elif cpu_score >= 25 and gpu_score >= 18:

            message = (
                "Your build should handle moderate 3D workloads."
            )

            status = "good"

        else:

            message = (
                "Your build may struggle with demanding 3D rendering. "
                "Consider upgrading the CPU or GPU."
            )

            status = "warning"

    elif usage == "general":

        if cpu_score >= 20 and ram_capacity >= 16:

            message = (
                "Your build is more than capable for general use, "
                "web browsing, office work and everyday applications."
            )

            status = "excellent"

        else:

            message = (
                "Your build should handle basic everyday tasks."
            )

            status = "good"

    else:

        return {
            "usage": usage,
            "status": "warning",
            "message": "Unknown usage selected."
        }

    return {
        "usage": (
            "Gaming" if usage == "gaming"
            else "Programming" if usage == "programming"
            else "Video Editing" if usage == "editing"
            else "3D / Rendering" if usage == "3d"
            else "General Use"
        ),
        "status": status,
        "message": message
    }