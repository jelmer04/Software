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
                write = "{:d},{:d},{},{},{},{},{},\n".format(i, j, line[1][0], line[1][1], line[2][0], line[2][1],z)
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