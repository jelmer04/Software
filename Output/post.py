'''
Write in the format:

        A,B,C,D,E,

            A = x axis position
            B = y axis position
            C = Printing required? (ie extruder motor running)
            D = end of island section?
            E = end of layer?
'''



def newfile(filename):
    """
    Create a new empty file

    :param filename: file to create
    """
    # Open the new file for writing
    with open(filename, "w") as file:
        pass
# End of function newfile()


def path(filename, path):
    """
    Write a path to the file

    :param filename:    file name to write
    :param path:        list of lines to write
    """

    # If the line is not empty:
    if len(path) > 0:
        # Open the file for appending
        with open(filename, "a") as file:
            # Define format string
            write = "{:.2f},{:.2f},{:d},{:d},{:d},\n"

            # Find the first point
            first = path[0]
            # Write the first point with "no extruding" option
            file.write(write.format(float(first[1][0]), float(first[1][1]), 0, 0, 0))

            # For each line in the path
            for i, line in enumerate(path):
                # If line isn't a repeated point
                if True or (line[1][0] != line[2][0]) and (line[1][1] != line[2][1]):

                    # If the line is somewhere in the middle of the list write it with "extruding" option
                    if i < len(path) - 1:
                        file.write(write.format(float(line[2][0]), float(line[2][1]), 1, 0, 0))

                    # If the line is the last of the path, write it with "extruding" and "end of island" options
                    else:
                        file.write(write.format(float(line[2][0]), float(line[2][1]), 1, 1, 0))
# End of function path()


def endlayer(filename):
    """
    Change the last line of the file to set the "end of layer" option

    :param filename: file name to write to
    """

    # Open file for reading, and read final ine
    with open(filename, "r") as file:
        lines = file.readlines()

    # Modify final line to include "end of layer" option
    lines[-1] = lines[-1][:-3] + "1,\n"

    # Open file and write modified line back to file
    with open(filename, "w") as file:
        file.writelines(lines)
# End of function endlayer()