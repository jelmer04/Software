def csv(linelist, filename):
    """
    Generate a csv file containing the x, y points in the list given

    @param linelist:    list of lines in the format [(normal), (point), (point)]...
    @param filename:    file to use - will be overwritten without warning
    @return:            none
    """
    with open(filename, "w") as file:
        for line in linelist:
            write = "{},{},{},{},\n".format(line[1][0], line[1][1], line[2][0], line[2][1])
            file.write(write)
            #print(write)
        return
# End of function csv()
