from decimal import Decimal


def nameslist():
    """
    Returns a list of parameter names

    :return: list of names
    """

    return ["part_file", "output_file", "slice_start", "slice_stop", "slice_step", "perim_count", "fill_angle",
            "fill_spacing", "nozzle_dia", "plotter_scale"]
# End of function nameslist()

def types(i):
    """
    Returns the type of the parameter at index i

    Key:
        f - file
            fx - existing file
            fm - empty file
            fa - ask if file exists
        d - decimal
        i - integer

    :param i: index to return type of
    :return:  type of parameter
    """

    return ["fx", "fa", "d", "d", "d", "i", "i", "d", "d", "i"][i]
# End of function types()


def load(filename):
    """
    Load parameters from specified file

    :param filename:    path to parameter file
    :return:            list of parameter values
    """
    params = ["", "", 0, 0, 1, 1, 0, 1, 1, 40]
    names = nameslist()

    # Open the file for reading
    with open(filename, "r") as file:
        # Check every line for parameter names
        for line in file:
            # Clean spaces and split at first colon
            line = line.strip()
            line = line.split(":", 1)
            # Search the list of parameter names for any matches
            for i, (param, name) in enumerate(zip(params, names)):
                if line[0] == name:
                    # Convert the parameter into the desired format
                    if types(i)[0] == "f":
                        params[i] = line[1].strip()
                    elif types(i)[0] == "d":
                        params[i] = Decimal(line[1].strip())
                    elif types(i)[0] == "i":
                        params[i] = int(line[1].strip())
                    else:
                        params[i] = line[1].strip()

    # Test whether files exist
    # Loop through every file
    for i, (param, name) in enumerate(zip(params, names)):
        # File must exist
        if types(i) == "fx":
            if not check_file(param):
                message("Error!", param+" does not exist!", True, ["OK"])
        # File must not exist
        elif types(i) == "fm":
            if check_file(param):
                message("Error!", param+" already exists!", True, ["OK"])
        # Ask what to do if file already exists
        elif types(i) == "fa":
            if check_file(param):
                message("Warning!", param+" already exists, overwrite?", False, ["Yes", "No"])

    print(tuple((n, p) for (n, p) in zip(names, params)))
    return params
# End of function load()


def get(params, name):
    """
    Get a specific parameter from the list

    :param params:  pre-populated list of parameters
    :param name:    name of parameter to extract
    :return:        parameter value
    """

    # Search for matching name in name list
    names = nameslist()
    for n, p in zip(names, params):
        if n == name:
            return p
    return
# End of function get()


def check_file(filename):
    """
    Check if file exists

    :param filename:    file to check
    :return:            boolean
    """

    # Try to open the file
    try:
        with open(filename):
            pass
        # File exists
        exists = True
    except FileNotFoundError:
        # File does not exist
        exists = False

    return exists
# End of function check_file()


def message(title="Message", text="Text", fatal=True, buttontext=["No", "Yes"], result=[False, True]):
    """
    Display a message window

    :param title:       message title                   - NOT IMPLEMENTED
    :param text:        message body
    :param fatal:       whether false response is fatal - NOT IMPLEMENTED
    :param buttontext:  list of labels for the buttons  - NOT IMPLEMENTED
    :param result:      list of return values           - NOT IMPLEMENTED
    :return:            value from result               - NOT IMPLEMENTED
    """
    print(text)
    if fatal:
        quit()
    return
# End of function message()