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
            "message": "Not enough CPU or GPU specifications to determine performance balance."
        }

    ratio = gpu_score / cpu_score

    if 0.5 <= ratio <= 1.0:

        return {
            "status": "balanced",
            "message": "The CPU and GPU provide a balanced performance combination."
        }

    elif ratio > 1.0:

        return {
            "status": "cpu_limited",
            "message": "The GPU is significantly stronger than the CPU and may be limited by the CPU in some workloads."
        }

    else:

        return {
            "status": "gpu_limited",
            "message": "The CPU is significantly stronger than the GPU and the GPU may limit graphical performance."
        }