def remove_duplicates(linelist):
    """
    Remove duplicate line points, irrespective of line normal

    @param linelist:
    @return:
    """
    i = 0
    while True:
        for line in linelist[i+1:]:
            a = linelist[i][1:]
            b = line[1:]
            if a == b or (a[0] == b[1] and a[1] == b[0]):
                linelist.pop(linelist.index(line))
        i += 1
        if i >= len(linelist):
            break
    return linelist
# End of function remove_duplicates()


def count_points(linelist):
    """
    Count the number of times each point appears in the list of lines

    @param linelist:    list of lines
    @return:            list of points and counters [(point), counter]...
    """
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
    return pointcounter
# End of function count_points()


def chop(linelist):
    """
    Break a list of lines into separate islands

    @param linelist:    list of line points [(normal), (point, (point)]...
    @return:            list of islands each consisting of a list of lines
    """

    linelist = remove_duplicates(linelist)

    pointcounter = count_points(linelist)

    #print("Point Count:", pointcounter)

    # Find the triple-point coordinate
    extrapoints = []
    overlaps = set()
    for point in pointcounter:
        # If there are an odd number of points
        if point[1] % 2 == 1:
            extrapoints.append(point[0])

        # If there are more than one pair of the point (point appears more than once on the path)
        elif point[1] > 2:
            print("Path overlaps at", point[0])
            overlaps.add(point[0])

    # Remove the extra lines if present
    if len(extrapoints) > 0:
        print("Extra Points:", extrapoints)
        i = 0
        # As long as there are still lines check
        while i < len(linelist):
            line = linelist[i][1:]
            count = 0
            # Check the current line against the extra points
            for point in extrapoints:
                if point in line:
                    count += 1
                #print(point, line, count)
            # If both points were marked for removal, remove the line
            if count == 2:
                print("Removed", line)
                linelist.pop(i)
            else:
                i += 1

        #print("Repaired Count:", count_points(linelist))

    islands = []
    while len(linelist) > 0:
        start = linelist[0][1]
        search = linelist[0][2]
        island = [linelist.pop(0)]
        i = 0
        #print("Starting at:", start)

        while i < len(linelist):
            line = linelist[i]
            i += 1
            #print("Searching for:", search, "in", line[1], line[2])
            retry = False
            if line[1] == search:
                if line[1] in overlaps:
                    dot = sum(a*b for (a, b) in zip(line[0][:2], island[-1][0][:2]))

                    print("Dot:", dot)

                    if dot < 0:
                        print("Not a good match, try again.")
                        retry = True

                if not retry:
                    search = line[2]
                    #print("Found it!")
                    i = 0
                    island.append(linelist.pop(linelist.index(line)))

            elif line[2] == search:
                if line[2] in overlaps:
                    dot = sum(a*b for (a, b) in zip(line[0][:2], island[-1][0][:2]))

                    print("Dot:", dot)

                    if dot < 0:
                        print("Not a good match, try again.")
                        retry = True

                if not retry:
                    search = line[1]
                    #print("Found it!")
                    i = 0
                    island.append(linelist.pop(linelist.index(line)))

            #print("Current island:", island)

            if search == start:
                #print("Found island:", island)
                islands.append(island)
                break

    return islands
# End of function chop()


def clockwise(linelist):
    """
    Sort a list of lines into clockwise order, by swapping line ends and normals

    @param linelist:    list of lines
    @return:            reordered list of lines
    """

    reverse = False
    for i, line in enumerate(linelist):
        sub = lambda a, b: ((a[0] - b[0]), (a[1] - b[1]))

        direction = sub(line[1], line[2])
        normal = (direction[1], -direction[0])

        #print(normal, line[0])
        #print(normal[0] * line[0][0], normal[1] * line[0][1])
        if normal[0] * line[0][0] >= 0 and normal[1] * line[0][1] >= 0:
            # In clockwise order
            pass
        else:
            # In anti-clockwise order
            linelist[i] = [line[0], line[2], line[1]]
            # If the first line is anti-clockwise, the entire list is backwards
            if i == 0:
                reverse = True

    if reverse:
        linelist.reverse()

    return linelist
# End of function clockwise()


def isclockwise(linelist):
    sub = lambda a, b: ((a[0] - b[0]), (a[1] - b[1]))

    clock = False

    for line in linelist:
        direction = sub(line[1], line[2])
        normal = (direction[1], -direction[0])

        #print(normal, line[0])
        #print(normal[0] * line[0][0], normal[1] * line[0][1])
        if normal[0] * line[0][0] >= 0 and normal[1] * line[0][1] >= 0:
            clock = True
        else:
            pass

    return clock


def splice(linelist, index):
    """
    Splice a list of lines at specified index

    @param linelist:    list of lines
    @param index:       index to splice at
    @return:            list of lines starting from index
    """
    index = index % len(linelist)
    output = linelist[index:]
    output.extend(linelist[:index])
    return output
# End of function splice()


def merge(linelist):
    """
    Merges all adjacent coincident lines

    :param linelist:    list of lines to merge
    :return:            list of lines, merged
    """
    i = 0
    while i < len(linelist):
        if linelist[i-1][0] == linelist[i][0]:
            # New line is normal, start of previous line, end of current line
            linelist[i] = (linelist[i][0], linelist[i-1][1], linelist[i][2])
            linelist.pop(i-1)
        i+=1
    return linelist


def short(linelist, length = 0.05):
    mag = lambda A, B: sum((a - b) ** 2 for (a, b) in zip(A, B))
    i = 0
    while i < len(linelist):
        line = linelist[i]
        last = linelist[i-1]
        if mag(line[2], last[1]) < length**2:

            linelist.pop(i)
            linelist[i-1][2] = line[2]
        else:
            i += 1

    return linelist
