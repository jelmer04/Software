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

    for i, line in enumerate(linelist):
        last = linelist[i-1]
        #print("Trimming", line[1:], last[1:])

        #print("Intersect:", line[1], sub(line[2], line[1]), last[1], sub(last[2], last[1]))
        intersection = intersect(line[1], sub(line[2], line[1]), last[2], sub(last[1], last[2]), Decimal(0.1))

        #intersection = tuple(Decimal((a+b)/2) for (a, b) in zip(line[1], last[2]))

        #print("Intersection at", intersection)

        linelist[i][1] = intersection
        linelist[i-1][2] = intersection

    #print("Trimmed to:", linelist)

    return linelist


def uncross(linelist):
    lim = lambda x: (min((x[1][0], x[2][0])), max((x[1][0], x[2][0])),
                     min((x[1][1], x[2][1])), max((x[1][1], x[2][1])))

    for i, line in enumerate(linelist):
        limits = lim(line)
        j = i
        while j < len(linelist):
            search = linelist[j]
            if (not i - 1 < j < i + 1) and\
                    (limits[0] < search[1][0] < limits[1] or limits[0] < search[2][0] < limits[1]) and\
                    (limits[2] < search[1][1] < limits[3] or limits[2] < search[2][1] < limits[3]):
                print("Self-intersecting:", line[1:], search[1:])

                linelist = linelist[:i] + linelist[j:]

            else:
                j += 1

    return linelist


def intersect(posa, dira, posb, dirb, max=100000):

    if (dira[1] == 0 and dirb[1] == 0) \
            or ((dira[1] != 0 and dirb[1] != 0) and (dira[0] / dira[1] == dirb[0] / dirb[1])) \
            or (posa == posb):
        return posb

    k = ((posa[0] * dirb[1]) - (posa[1] * dirb[0]) + (posb[1] * dirb[0]) - (posb[0] * dirb[1]))
    l = ((dira[1] * dirb[0]) - (dira[0] * dirb[1]))

    #if abs(k) > max:
    #    k = int(k)

    #if abs(l) > max:
    #    l = int(l)

    #print("K =", abs(round(k, 3)), "L =", abs(round(l, 3)))

    if abs(round(l, 3)) == 0:
        #print("L is zero")
        return posb
    if abs(round(k, 3)) == 0:
        #print("K is zero")
        return posb
    else:
        #print("K and L both non-zero")
        k = Decimal(k / l)

    if abs(k) > max:
        #print("Using average point")
        return tuple((a + b)/2 for (a, b) in zip(posa, posb))
    else:
        #print("Using intersect point", k)
        pass

    point = tuple (k * a for a in dira)
    point = tuple (p + a for (p, a) in zip(point, posa))
    return point


def magnitude(vector):
    """
    Calculate the magnitude (length) of the vector given

    @param vector:  vector points
    @return:        scalar magnitude
    """
    squares = (Decimal(v**2) for v in vector)
    mag = Decimal(str(round(sum(squares).sqrt(), 2)))
    return mag