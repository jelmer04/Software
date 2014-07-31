from decimal import Decimal
from tkinter import *
from tkinter import ttk


def nameslist():
    return ["part_file", "output_file", "slice_start", "slice_stop", "slice_step", "perim_count", "fill_angle",
            "fill_spacing", "nozzle_dia"]

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
    return ["fx", "fa", "d", "d", "d", "i", "i", "d", "d"][i]


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
                message("Error!", param+" does not exist!", ["OK"])
        elif types(i) == "fe":
            if check_file(param):
                message("Error!", param+" already exists!", ["OK"])
        elif types(i) == "fa":
            if check_file(param):
                message("Warning!", param+" already exists, overwrite?", ["Yes", "No"])

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


def message(title="Message", text="Text", buttontext=["No", "Yes"], result=[False, True]):

    root = Tk()
    root.title(title)

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    #feet = StringVar()
    #meters = StringVar()

    #feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
    #feet_entry.grid(column=2, row=1, sticky=(W, E))

    ttk.Label(mainframe, text=text).grid(column=1, row=1, sticky=(W, E), columnspan=len(buttontext))

    buttons = []
    for b, button in enumerate(buttontext):
        buttons.append(ttk.Button(mainframe, text=button).grid(column=b+1, row=2, sticky=W))

    #ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
    #ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
    #ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    #buttons[0].focus()
    #root.bind('<Return>')

    root.mainloop()

    return 0