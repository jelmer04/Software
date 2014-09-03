def csv_islands(filename, islands, z):
    """
    Write to a CSV file containing the x, y points in the list given

    @param linelist:    list of lines in the format [(normal), (point), (point)]...
    @param filename:    file to use
    @return:            none
    """
    with open(filename, "a") as file:
        for i, island in enumerate(islands):
            for j, line in enumerate(island):
                write = "{:d},{:d},{},{},{},{},{},\n".format(i, j, line[1][0], line[1][1], line[2][0], line[2][1], z)
                file.write(write)
                #print(line)
                #print(write)

        return
# End of function csv()


def csv_header(filename):
    """
    Creates a CSV file with header row

    :param filename:    file to write to
    """
    with open(filename, "w") as file:
        header = "Island,Line,Start-X,Start-Y,End-X,End-Y,Z,\n"
        file.write(header)
# End of function csv_header()


def newfile(filename):
    """
    Creates a new file with a title

    :param filename:
    """
    with open(filename, "w") as file:
        file.write("///\n/// sliced output\n///\n\n")
# End of function newfile()


def path(filename, path):
    """
    Writes a humanly readable list of lines in the form: from A to B

    :param filename:    file to write to
    :param path:        list of lines to write
    """
    if len(path) > 0:
        with open(filename, "a") as file:
            file.write("new path\n")
            for line in path:
                write = "\tfrom ({:.2f},{:.2f}) \t to ({:.2f},{:.2f})\n".\
                        format(float(line[1][0]), float(line[1][1]), float(line[2][0]), float(line[2][1]))
                file.write(write)
            file.write("\n")
# End of function path()


def layer(filename, layer):
    """
    Write a humanly readable line to start a new layer

    :param filename:    file to write to
    :param layer:       Z-height of the layer
    """
    with open(filename, "a") as file:
        file.write("new layer at {}\n".format(layer))
# End of function layer()