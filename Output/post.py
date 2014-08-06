'''
Write in the format:

        [A,B,C,D,E]

            A = x axis position
            B = y axis position
            C = Printing required? (ie extruder motor running)
            D = end of island section?
            E = end of layer?
'''



def newfile(filename):
    with open(filename, "w") as file:
        pass


def path(filename, path):
    if len(path) > 0:
        with open(filename, "a") as file:
            write = "{:.2f},{:.2f},{:d},{:d},{:d}\n"

            line = path[0]
            # First point in a line
            file.write(write.format(float(line[1][0]), float(line[1][1]), 0, 0, 0))

            for i, line in enumerate(path):
                if i < len(path) - 1:
                    file.write(write.format(float(line[2][0]), float(line[2][1]), 1, 0, 0))
                else:
                    file.write(write.format(float(line[2][0]), float(line[2][1]), 1, 1, 0))


def endlayer(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    lines[-1] = lines[-1][:-2] + "1\n"

    with open(filename, "w") as file:
        file.writelines(lines)
