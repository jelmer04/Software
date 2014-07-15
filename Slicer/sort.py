def chop(linelist):
    """
    Break a line into separate islands

    @param linelist:    list of line points [(normal), (point, (point)]...
    """

    # Remove duplicates??
    i = 0
    while True:
        for line in linelist[i+1:]:
            if linelist[i][1:] == line[1:]:
                linelist.pop(linelist.index(line))
                print(line)
        i += 1
        if i <= len(linelist):
            break
    pointcounter = []

    for [n, a, b] in linelist:
        for x in [a, b]:
            duplicate = False
            for point in pointcounter:
                if point[0] == x:
                    duplicate = True
                    point[1] += 1
            if not duplicate:
                pointcounter.append([x, 1])

    extrapoints = []
    for point in pointcounter:
        if point[1] > 2:
            extrapoints.append(point[0])


    return pointcounter
