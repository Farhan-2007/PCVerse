from app.specification_parser import parse_specification


def get_cpu_performance(cpu):

    if not cpu or not cpu.specification:
        return 0

    specs = parse_specification(cpu.specification)

    cores = specs.get("Cores")
    boost_clock = specs.get("Boost Clock")

    if not cores or not boost_clock:
        return 0

    cores = int(cores)

    boost_clock = float(
        boost_clock.replace("GHz", "").strip()
    )

    return cores * boost_clock


def get_gpu_performance(gpu):

    if not gpu or not gpu.specification:
        return 0

    specs = parse_specification(gpu.specification)

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


def check_cpu_gpu_performance(cpu, gpu):

    cpu_score = get_cpu_performance(cpu)
    gpu_score = get_gpu_performance(gpu)

    if cpu_score == 0 or gpu_score == 0:

        return {
            "status": "unknown",
            "message": "CPU or GPU performance specifications are missing."
        }

    ratio = gpu_score / cpu_score

    if ratio > 2.0:

        return {
            "status": "cpu_limited",
            "message": (
                "The GPU is significantly stronger than the CPU. "
                "A stronger CPU may provide better overall balance."
            )
        }

    elif ratio < 0.7:

        return {
            "status": "gpu_limited",
            "message": (
                "The CPU is significantly stronger than the GPU. "
                "A stronger GPU may improve gaming performance."
            )
        }

    else:

        return {
            "status": "balanced",
            "message": (
                "The CPU and GPU are reasonably well balanced "
                "for this build."
            )
        }