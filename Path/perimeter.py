from decimal import Decimal

def offset(linelist, offset):

    for i, (n, a, b) in enumerate(linelist):
        mag = magnitude(n)
        if mag != 1:
            n = (z / mag for z in n)

        a = tuple(x - y * offset for (x, y) in zip(a, n))
        b = tuple(x - y * offset for (x, y) in zip(b, n))
        linelist[i] = [n, a, b]

    return list(linelist)


def trim(linelist):
    sub = lambda x, y: ((x[0] - y[0]), (x[1] - y[1]))

    for i, line in enumerate(linelist):
        last = linelist[i-1]
        #print("Trimming", line[1:], last[1:])
        #print("Intersect:", line[1], sub(line[2], line[1]), last[1], sub(last[2], last[1]))
        intersection = intersect(line[1], sub(line[2], line[1]), last[2], sub(last[1], last[2]))

        #print("Intersection at", intersection)

        linelist[i][1] = intersection
        linelist[i-1][2] = intersection

    return linelist


def intersect(posa, dira, posb, dirb):

    if (dira[1] == 0 and dirb[1] == 0) \
            or ((dira[1] != 0 and dirb[1] != 0) and (dira[0] / dira[1] == dirb[0] / dirb[1])) \
            or (posa == posb):
        return posb

    k = ((posa[0] * dirb[1]) - (posa[1] * dirb[0]) + (posb[1] * dirb[0]) - (posb[0] * dirb[1])) \
        / ((dira[1] * dirb[0]) - (dira[0] * dirb[1]))

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