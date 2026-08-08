def parse_specification(specification):

    specs = {}

    if not specification:
        return specs

    lines = specification.split("\n")

    for line in lines:

        if ":" in line:

            key, value = line.split(":", 1)

            key = key.strip()
            value = value.strip()

            specs[key] = value

    return specs


if __name__ == "__main__":

    test_specification = """Socket: AM5
Cores: 8
Threads: 16
Base Clock: 4.5 GHz
Boost Clock: 5.4 GHz
TDP: 105W"""

    result = parse_specification(test_specification)

    print(result)