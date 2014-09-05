from decimal import Decimal
from shapely import geometry


def polygon(linelist):
    """
    Convert a line list into a Shapely polygon

    :param linelist:
    :return:
    """

    # Start the list of points
    pointlist = [linelist[0][1]]
    # Append each end point to the list
    for line in linelist:
        pointlist.append(line[2])

    # Convert points list into polygon
    return geometry.Polygon(pointlist)
# End of function polygon()


def merge(a, b):
    """
    Merges polygons a and b using symmetric difference

    :param a:   polygon to merge
    :param b:   polygon to merge
    :return:    merged polygon
    """
    return a.symmetric_difference(b)
# End of function merge()


def linepoly(poly):
    """
    Converts a polygon to a list of lines

    :param poly:    polygon to convert
    :return:        list of lines
    """

    # If the polygon consists of multiple islands
    linelist = []
    if poly.geom_type == "MultiPolygon":
        for p in poly:
            # Extract the coordinates from each island and append them
            linelist.extend(lineinterior(p))
        return linelist
    # If theres only one island
    else:
        # Extract the coordinates
        return lineinterior(poly)
# End of function linepoly()


def lineexterior(poly):
    """
    Extract the exterior coordinates

    :param poly:    polygon to extract from
    :return:        list of coordinates
    """

    # If the polygon is a ring, convert it to a polygon
    if poly.geom_type == "LinearRing":
        poly = geometry.Polygon(poly)

    # Extract the polygon exterior coordinates
    coords = list(poly.exterior.coords)
    # Generate a list of lines
    linelist = []
    for i, p in enumerate(coords[:-1]):
        # Start point
        p = tuple(Decimal(x) for x in p)
        # End point
        q = tuple(Decimal(x) for x in coords[i + 1])
        # Calculate the magnitude of the start point (for unit vector calculation)
        mag = magnitude(p)
        if mag == 0:
            mag = 1
        # Calculate the normals
        n = tuple(Decimal(a - b) / mag for a, b in zip(p, q))
        n = [n[1], -n[0]]
        # Append the new line
        linelist.append([n, p, q])
    return linelist
# End of function lineexterior()


def lineinterior(poly):
    """
    Extract the interior and exterior points from a polygon

    :param poly:    polygon to extract coordinates from
    :return:        list
    """

    # Extract the exterior
    linelist = lineexterior(poly)
    for p in poly.interiors:
        linelist.extend(lineexterior(p))
    return linelist
# End of function lineinterior()


def normals(linelist):
    """
    Calculate normals for a list of lines

    :param linelist:    list of lines
    :return:            list of liens with newly calculated normals
    """
    for i, (n, *points) in enumerate(linelist):
        x = points[0][0] > points[1][0]
        y = points[0][1] > points[1][1]

        # print(i, x, y)

        if not x and not y:
            n = [n[0], -n[1]]
        elif x and not y:
            n = [n[0], -n[1]]
        elif x and y:
            n = [n[0], -n[1]]
        elif not x and y:
            n = [n[0], -n[1]]
        else:
            #print("Zero", i, x, y)
            n = [0, 0]

        #print(n)
        linelist[i][0] = tuple(n)

    return linelist


def offset(linelist, distance):
    try:
        if linelist.geom_type:
            pass
        poly = linelist
    except:
        poly = polygon(linelist)

    poly = poly.buffer(-distance)

    # if poly.geom_type == "MultiPolygon":
    #    poly = poly[0]

    return (poly)


# for i, (n, a, b) in enumerate(linelist):
#        mag = magnitude(n[:2])
#        if mag != 1:
#            n = tuple(z / mag for z in n)
#
#        a = tuple((a[0] - n[0] * distance, a[1] - n[1] * distance))
#        b = tuple((b[0] - n[0] * distance, b[1] - n[1] * distance))
#
#        #print("New line:", a, b)
#        linelist[i] = [n, a, b]
#
#    return list(linelist)


def trim(linelist):
    """
    Takes a list of lines and finds the intersections between adjacent pairs

    :param linelist:    list of lines
    :return:            list of trimmed lines
    """

    firstpass = 0.3
    searchpass = 0.1

    sub = lambda x, y: ((x[0] - y[0]), (x[1] - y[1]))

    nonintersections = []
    intersections = []
    i = 0

    while i < len(linelist):
        line = linelist[i]
        last = linelist[i - 1]
        #print("Trimming", line[1:], last[1:])

        #print("Intersect:", line[1], sub(line[2], line[1]), last[1], sub(last[2], last[1]))
        intersection = intersect(line[1], sub(line[2], line[1]), last[2], sub(last[1], last[2]),
                                 "abs " + str(firstpass))

        #intersection = tuple(Decimal((a+b)/2) for (a, b) in zip(line[1], last[2]))

        #print("Intersection at", intersection)

        if intersection:
            linelist[i][1] = intersection
            linelist[i - 1][2] = intersection
            intersections.append([i - 1, i])
        else:
            #print("Lines don't intersect:", line[1:], last[1:])
            nonintersections.append([i - 1, i])
        i += 1


    # Group lines
    i = 0
    while i < len(intersections):
        pair = intersections[i]
        last = intersections[i - 1]

        if pair[0] == last[-1]:
            last.append(pair[1])
            intersections.pop(i)
        else:
            i += 1

    print(intersections)

    print(nonintersections)

    removals = []

    for i, pair in enumerate(nonintersections):
        fixed = False

        print("Trying to fix", pair)

        # Find intersections with first point
        print("Searching with first point")
        search = linelist[pair[0]]

        for j in range(pair[-1] + 1, len(linelist)):

            if j >= len(linelist):
                j -= (len(linelist) + 1)

            line = linelist[j]
            intersection = intersect(line[1], sub(line[2], line[1]), search[2], sub(search[1], search[2]),
                                     "abs " + str(searchpass))
            #print(j, intersection)
            if intersection:
                print("Fixing", pair, intersection)
                linelist[pair[0]][2] = intersection
                linelist[j][1] = intersection

                removals.extend(range(pair[0] + 1, j))
                fixed = True
                break

        if not fixed:

            # Find intersections with second point
            print("Searching with second point")
            search = linelist[pair[-1]]

            for j in range(0, pair[0]):

                if j >= len(linelist):
                    j -= (len(linelist) + 1)

                line = linelist[j]
                intersection = intersect(line[1], sub(line[2], line[1]), search[2], sub(search[1], search[2]),
                                         "abs " + str(searchpass))
                #print(j, intersection)
                if intersection:
                    print("Fixing", pair, intersection)
                    linelist[pair[-1]][1] = intersection
                    linelist[j][2] = intersection

                    removals.extend(range(j + 1, pair[-1]))
                    fixed = True
                    break

        if not fixed:
            print("Couldn't fix", pair)

    removals = list(set(removals))
    removals.sort()
    print("Remove:", removals)
    for i, r in enumerate(removals):
        if r - i < len(linelist):
            #linelist[r] = [(Decimal('0'), Decimal('0'), Decimal('0')), (Decimal('0'), Decimal('0')), (Decimal('0'), Decimal('0'))]
            linelist.pop(r - i)
            pass

    #print("Trimmed to:", linelist)


    return linelist


def uncross(linelistin):
    lim = lambda x: [(min((x[1][0], x[2][0])), max((x[1][0], x[2][0]))),
                     (min((x[1][1], x[2][1])), max((x[1][1], x[2][1])))]

    linelist = xorder(linelistin[:])

    intersections = []

    for i, line in enumerate(linelist):
        j = i + 1
        while j < len(linelist):
            search = linelist[j]
            if \
                                                            line[1][0] < search[1][0] < line[2][0] or \
                                                            line[1][0] < search[2][0] < line[2][0] or \
                                                    search[1][0] < line[1][0] < search[2][0] or \
                                            search[1][0] < line[2][0] < search[2][0]:

                #print(i, j, "Overlapping X:", line[1][0], line[2][0], search[1][0], search[2][0])

                liney = line[:]
                if liney[1][1] > liney[2][1]:
                    liney = (liney[0], liney[2], liney[1])

                searchy = search[:]
                if searchy[1][1] > search[2][1]:
                    search = (search[0], search[2], search[1])

                if \
                                                                liney[1][1] < searchy[1][1] < liney[2][1] or \
                                                                liney[1][1] < searchy[2][1] < liney[2][1] or \
                                                        searchy[1][1] < liney[1][1] < searchy[2][1] or \
                                                searchy[1][1] < liney[2][1] < searchy[2][1]:
                    #print(i, j, "Overlapping Y:", line[1][1], line[2][1], search[1][1], search[2][1])

                    #print("Overlapping!!", line[1:], search[1:])

                    intersections.append((i, j))
            j += 1

    print("Crosses:", intersections)
    return linelistin


def xorder(linelist):
    for i, line in enumerate(linelist):
        if line[1][0] > line[2][0]:
            linelist[i] = [line[0], line[2], line[1]]

    linelist.sort(key=lambda x: x[1][0])
    return linelist


def intersect(posa, dira, posb, dirb, mode="extend"):
    """
    Finds the intersection point of two vectors:

    Mode:   extend  - extend the line infinitely
            shorten - only shorten the line
            limit x - proportionally extend up to +/-x
            abs x   - extend up to absolute length of +/- x

    :param posa:
    :param dira:
    :param posb:
    :param dirb:
    :param mode:
    :return:
    """
    if dira[1] == 0 and dirb[1] == 0 and posa != posb \
            or ((dira[1] != 0 and dirb[1] != 0) and (dira[0] / dira[1] == dirb[0] / dirb[1])):
        return False

    if (dira[1] == 0 and dirb[1] == 0) \
            or (posa == posb):
        print("Unable to calculate intersection")
        return posb

    k1 = ((posa[0] * dirb[1]) - (posa[1] * dirb[0]) + (posb[1] * dirb[0]) - (posb[0] * dirb[1]))
    l1 = ((dira[1] * dirb[0]) - (dira[0] * dirb[1]))
    k2 = ((posb[0] * dira[1]) - (posb[1] * dira[0]) + (posa[1] * dira[0]) - (posa[0] * dira[1]))
    l2 = ((dirb[1] * dira[0]) - (dirb[0] * dira[1]))

    #print("K =", abs(round(k1, 3)), "L =", abs(round(l1, 3)))

    if k1 == 0 or k2 == 0:
        return False

    k1 = Decimal(k1 / l1)
    k2 = Decimal(k2 / l2)

    #print("K =", k1, k2)

    limit = 0
    if mode.startswith("limit"):
        mode = mode.split()
        limit = Decimal(mode[1])
        mode = mode[0]
    elif mode.startswith("abs"):
        mode = mode.split()
        limit = Decimal(mode[1])
        try:
            limit1 = limit / magnitude(dira)
        except:
            limit1 = 0
        try:
            limit2 = limit / magnitude(dirb)
        except:
            limit2 = 0
        mode = mode[0]

    #print("Limit =", limit)

    if mode == "extend" or \
            (mode == "abs" and \
                     (-limit1 <= k1 <= Decimal(1 + limit1) and -limit2 <= k2 <= Decimal(1 + limit2))) or \
            ((mode == "shorten" or mode == "limit") and \
                     (-limit <= k1 <= Decimal(1 + limit) and -limit <= k2 <= Decimal(1 + limit))):
        point = tuple(k1 * a for a in dira)
        point = tuple(p + a for (p, a) in zip(point, posa))
        return point
    else:
        return False


def magnitude(vector):
    """
    Calculate the magnitude (length) of the vector given

    @param vector:  vector points
    @return:        scalar magnitude
    """
    squares = (Decimal(v ** 2) for v in vector)
    mag = Decimal(str(round(sum(squares).sqrt(), 2)))
    return mag