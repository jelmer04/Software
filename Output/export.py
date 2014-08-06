def csv_islands(filename, islands, z):
    """
    Generate a csv file containing the x, y points in the list given

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
    with open(filename, "w") as file:
        header = "Island,Line,Start-X,Start-Y,End-X,End-Y,Z,\n"
        file.write(header)
        return

def newfile(filename):
    with open(filename, "w") as file:
        file.write("///\n/// sliced output\n///\n\n")


def path(filename, path):
    if len(path) > 0:
        with open(filename, "a") as file:
            file.write("new path\n")
            for line in path:
                write = "\tfrom ({:.2f},{:.2f}) \t to ({:.2f},{:.2f})\n".\
                        format(float(line[1][0]), float(line[1][1]), float(line[2][0]), float(line[2][1]))
                file.write(write)
            file.write("\n")


def layer(filename, layer):
    with open(filename, "a") as file:
        file.write("new layer at {}\n".format(layer))