from decimal import Decimal


def nameslist():
    return ["part_file", "output_file", "slice_start", "slice_stop", "slice_step", "perim_count", "fill_angle",
            "fill_spacing", "nozzle_dia"]


def load(filename):
    params = ["", "", 0, 0, 1, 1, 0, 1, 1]
    names = nameslist()

    part_file = ""
    output_file = ""
    slice_start = 0
    slice_stop = 0
    slice_step = 1
    perim_count = 1
    fill_angle = 0
    fill_spacing = 1
    nozzle_dia = 1

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            line = line.split(":", 1)
            for i, (param, name) in enumerate(zip(params, names)):
                if line[0] == name:
                    if type(param) is str:
                        params[i] = line[1].strip()
                    else:
                        params[i] = Decimal(line[1].strip())
        print(tuple((n, p) for (n, p) in zip(names, params)))
        return params


def get(params, name):
    names = nameslist()
    for n, p in zip(names, params):
        if n == name:
            return p
    return
