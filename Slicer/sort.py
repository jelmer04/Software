def chop(linelist):
    """
    Break a line into separate islands

    @param linelist:    list of line points [(normal), (point, (point)]...
    """

    pointcounter = []
    for [n, a, b] in linelist:
        print("Points:", a, "\tand", b)
        for x in (a, b):

            duplicate = False
            for (y, c) in pointcounter:
                if y == x:
                    duplicate = True
                    print("Duplicate", x, y)

            if not duplicate:
                count = 0
                for [m, i, j] in linelist:

                    if x == i:
                        count += 1
                    if x == j:
                        count += 1
                    print(x, count, i, j)
                pointcounter.append((x, count))
            linelist.pop(0)

    return pointcounter
