from decimal import Decimal

def offset(linelist, distance):

    for i, (n, a, b) in enumerate(linelist):
        mag = magnitude(n[:2])
        if mag != 1:
            n = tuple(z / mag for z in n)

        a = tuple((a[0] - n[0] * distance, a[1] - n[1] * distance))
        b = tuple((b[0] - n[0] * distance, b[1] - n[1] * distance))

        #print("New line:", a, b)
        linelist[i] = [n, a, b]

    return list(linelist)


def trim(linelist):
    """
    Takes a list of lines and finds the intersections between adjacent pairs

    :param linelist:    list of lines
    :return:            list of trimmed lines
    """
    sub = lambda x, y: ((x[0] - y[0]), (x[1] - y[1]))

    nonintersections = []
    intersections = []
    i = 0

    while i < len(linelist):
        line = linelist[i]
        last = linelist[i-1]
        #print("Trimming", line[1:], last[1:])

        #print("Intersect:", line[1], sub(line[2], line[1]), last[1], sub(last[2], last[1]))
        intersection = intersect(line[1], sub(line[2], line[1]), last[2], sub(last[1], last[2]), "abs 0.25")

        #intersection = tuple(Decimal((a+b)/2) for (a, b) in zip(line[1], last[2]))

        #print("Intersection at", intersection)

        if intersection:
            linelist[i][1] = intersection
            linelist[i-1][2] = intersection
            intersections.append([i-1, i])
        else:
            #print("Lines don't intersect:", line[1:], last[1:])
            nonintersections.append([i-1, i])
        i += 1

    i = 0
    while i < len(intersections):
        pair = intersections[i]
        last = intersections[i-1]

        if pair[0] == last[-1]:
            last.append(pair[1])
            intersections.pop(i)
        else:
            i += 1

    i = 0
    while i < len(nonintersections):
        pair = nonintersections[i]
        last = nonintersections[i-1]

        if pair[0] == last[-1]:
            last.append(pair[1])
            nonintersections.pop(i)
        else:
            i += 1

    print(intersections)

    print(nonintersections)

    removals = []

    for i, pair in enumerate(nonintersections):
        fixed = False

        # Find intersections with first point
        print("Searching with first point", intersections[i + 1])
        search = linelist[pair[0]]

        for j in intersections[i + 1]:

            if j >= len(linelist):
                j -= (len(linelist)+1)

            line = linelist[j]
            intersection = intersect(line[1], sub(line[2], line[1]), search[2], sub(search[1], search[2]), "shorten")
            #print(j, intersection)
            if intersection:
                linelist[pair[0]][2] = intersection
                linelist[j][1] = intersection

                removals.extend(range(pair[0] + 1, j))
                fixed = True
                break

        if fixed:
            break

        # Find intersections with second point
        print("Searching with second point")
        search = linelist[pair[-1]]

        for j in intersections[i]:

            if j >= len(linelist):
                j -= (len(linelist)+1)

            line = linelist[j]
            intersection = intersect(line[1], sub(line[2], line[1]), search[2], sub(search[1], search[2]), "shorten")
            #print(j, intersection)
            if intersection:
                linelist[pair[-1]][1] = intersection
                linelist[j][2] = intersection

                removals.extend(range(j + 1, pair[-1]))
                fixed = True

    print("Lines:", len(linelist))

    removals = list(set(removals))
    print("Remove:", removals)
    for i, r in enumerate(removals):
        print(r)
        if r - i < len(linelist):
            #linelist.pop(r - i)
            pass

    #print("Trimmed to:", linelist)

    return linelist


def uncross(linelistin):
    lim = lambda x: [(min((x[1][0], x[2][0])), max((x[1][0], x[2][0]))),
                     (min((x[1][1], x[2][1])), max((x[1][1], x[2][1])))]

    linelist = xorder(linelistin[:])

    intersections = []

    for i, line in enumerate(linelist):
        j = i+1
        while j < len(linelist):
            search = linelist[j]
            if\
                          line[1][0] < search[1][0] <   line[2][0] or\
                          line[1][0] < search[2][0] <   line[2][0] or\
                        search[1][0] <   line[1][0] < search[2][0] or\
                        search[1][0] <   line[2][0] < search[2][0]:

                #print(i, j, "Overlapping X:", line[1][0], line[2][0], search[1][0], search[2][0])

                liney = line[:]
                if liney[1][1] > liney[2][1]:
                    liney = (liney[0], liney[2], liney[1])

                searchy = search[:]
                if searchy[1][1] > search[2][1]:
                    search = (search[0], search[2], search[1])

                if\
                          liney[1][1] < searchy[1][1] <   liney[2][1] or\
                          liney[1][1] < searchy[2][1] <   liney[2][1] or\
                        searchy[1][1] <   liney[1][1] < searchy[2][1] or\
                        searchy[1][1] <   liney[2][1] < searchy[2][1]:
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



def intersect(posa, dira, posb, dirb, mode = "extend"):
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
    if dira[1] == 0 and dirb[1] == 0 and posa != posb:
        return False

    if (dira[1] == 0 and dirb[1] == 0) \
            or ((dira[1] != 0 and dirb[1] != 0) and (dira[0] / dira[1] == dirb[0] / dirb[1])) \
            or (posa == posb):
        return posb

    k1 = ((posa[0] * dirb[1]) - (posa[1] * dirb[0]) + (posb[1] * dirb[0]) - (posb[0] * dirb[1]))
    l1 = ((dira[1] * dirb[0]) - (dira[0] * dirb[1]))
    k2 = ((posb[0] * dira[1]) - (posb[1] * dira[0]) + (posa[1] * dira[0]) - (posa[0] * dira[1]))
    l2 = ((dirb[1] * dira[0]) - (dirb[0] * dira[1]))

    #print("K =", abs(round(k1, 3)), "L =", abs(round(l1, 3)))

    if abs(round(l1, 3)) == 0:
        #print("L is zero")
        return posb
    if abs(round(k1, 3)) == 0:
        #print("K is zero")
        return posb
    else:
        #print("K and L both non-zero")
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
        limit1 = limit / magnitude(dira)
        limit2 = limit / magnitude(dirb)
        mode = mode[0]

    #print("Limit =", limit)

    if mode == "extend" or\
            (mode == "abs" and\
                     (-limit1 <= k1 <= Decimal(1 + limit1) and -limit2 <= k2 <= Decimal(1 + limit2))) or\
            ((mode == "shorten" or mode == "limit") and\
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
    squares = (Decimal(v**2) for v in vector)
    mag = Decimal(str(round(sum(squares).sqrt(), 2)))
    return mag