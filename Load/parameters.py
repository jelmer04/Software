from decimal import Decimal
from tkinter import *
from tkinter import messagebox


def nameslist():
    return ["part_file", "output_file", "slice_start", "slice_stop", "slice_step", "perim_count", "fill_angle",
            "fill_spacing", "nozzle_dia", "plotter_scale"]

def types(i):
    """
    Returns the type of the parameter at index i

    Key:
        f - file
            fx - existing file
            fe - empty file
            fa - ask if file exists
        d - decimal
        i - integer

    :param i: index to return type of
    :return:  type of parameter
    """
    return ["fx", "fa", "d", "d", "d", "i", "i", "d", "d", "i"][i]


def load(filename):
    params = ["", "", 0, 0, 1, 1, 0, 1, 1, 40]
    names = nameslist()

    # Defaults:
    #part_file = ""
    #output_file = ""
    #slice_start = 0
    #slice_stop = 0
    #slice_step = 1
    #perim_count = 1
    #fill_angle = 0
    #fill_spacing = 1
    #nozzle_dia = 1

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            line = line.split(":", 1)
            for i, (param, name) in enumerate(zip(params, names)):
                if line[0] == name:
                    if types(i)[0] == "f":
                        params[i] = line[1].strip()
                    elif types(i)[0] == "d":
                        params[i] = Decimal(line[1].strip())
                    elif types(i)[0] == "i":
                        params[i] = int(line[1].strip())
                    else:
                        params[i] = line[1].strip()

    for i, (param, name) in enumerate(zip(params, names)):
        if types(i) == "fx":
            if not check_file(param):
                message("Error!", param+" does not exist!", True, ["OK"])
        elif types(i) == "fe":
            if check_file(param):
                message("Error!", param+" already exists!", True, ["OK"])
        elif types(i) == "fa":
            if check_file(param):
                message("Warning!", param+" already exists, overwrite?", False, ["Yes", "No"])

    print(tuple((n, p) for (n, p) in zip(names, params)))
    return params


def get(params, name):
    names = nameslist()
    for n, p in zip(names, params):
        if n == name:
            return p
    return


def check_file(filename):
    try:
        with open(filename):
            pass
        exists = True
    except FileNotFoundError:
        exists = False

    return exists


def message(title="Message", text="Text", fatal=True, buttontext=["No", "Yes"], result=[False, True]):

    print(text)
    if fatal:
        quit()
    return

    root = Tk()
    root.wm_withdraw()

    messagebox.showinfo(title, text)
    return 0