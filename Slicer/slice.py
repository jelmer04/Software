import logging  # Message logging
from decimal import *


def snap(facetlist, precision=2):
    """
    Round a list of facets to specified precision - snap it to a grid!

    @param facetlist:   list of facets [(normal), (point), (point), (point)]
    @param precision:   number of decimal places
    @return:            list of rounded facets [(normal), (point), (point), (point)]
    """
    snaplist = []

    context = Context(prec=precision, rounding=ROUND_HALF_UP)

    for facet in facetlist:
        snapped = []
        for f in facet:
            snapped.append(snap_point(f, precision))
        snaplist.append(snapped)
    return snaplist
# End of function snap()


def snap_point(point, precision=2):
    return tuple(snap_number(x, precision) for x in point)


def snap_number(number, precision=2):
    return Decimal(str(round(number, precision)))


def layer(facetlist, depth):
    """
    Slices a geometry (list of facets) in the z plane at the specified depth.

    @type  facetlist:   list
    @param facetlist:   list of facets [(normal), (point), (point), (point)]
    @type  depth:       decimal
    @param depth:       z-depth to slice through
    @return:            list of lines [(normal), (point), (point)]
    """

    linelist = []

    for facet in facetlist:
        if facet != []:
            # Find whether the facet intersects the slice
            touch = [0, 0, 0]
            above = [0, 0, 0]
            below = [0, 0, 0]
            for i, point in enumerate(facet[1:]):
                if point[2] == depth:
                    touch[i] = 1
                elif point[2] > depth:
                    above[i] = 1
                elif point[2] < depth:
                    below[i] = 1
            logging.debug("Above: %d\tTouching: %d\tBelow: %d", sum(above), sum(touch), sum(below))

            # Intersection mode for debugging
            mode = 0
            # Find intersections:
            coords = [facet.pop(0)]
            if (sum(above) == 3) or (sum(below) == 3):  # points are all above or all below
                logging.debug("Facet does not intersect plane")

            else:
                logging.debug("Facet intersects plane")
                if sum(touch) == 3:  # MODE 5
                    mode = 5
                    # all on plane
                    coords.append(facet[1:])

                elif sum(touch) == 1:
                    if sum(above) == 1 and sum(below) == 1:  # MODE 2
                        mode = 2
                        # need to find one intersection
                        linepoints = facet[:]
                        coords.append(linepoints.pop(touch.index(1))[0:2])
                        coords.append(intersect(linepoints, depth))

                    elif sum(above) == 0 or sum(below) == 0:  # MODE 3
                        mode = 3
                        coords.append(tuple(facet[i][0:2]))
                        # already done this point as only one intersection!
                        coords.append(coords[0])

                elif sum(touch) == 2:  # MODE 4
                    mode = 4
                    facet.pop(touch.index(0))
                    coords.extend([tuple(facet[0][0:2]), tuple(facet[1][0:2])])

                elif sum(above) == 2 or sum(below) == 2:  # MODE 1
                    mode = 1

                    if sum(above) == 2:
                        pair = above[:]
                    else:
                        pair = below[:]

                    print(len(facet))
                    if len(facet) == 3:
                        linepoints = facet[:]
                        linepoints.pop(pair.index(1))

                        print("Intersect:", len(linepoints))

                        coords.append(intersect(linepoints, depth))

                        linepoints = facet[:]
                        linepoints.reverse()
                        pairReversed = pair[:]
                        pairReversed.reverse()

                        linepoints.pop(pairReversed.index(1))

                        coords.append(intersect(linepoints, depth))

            logging.debug("Facet intersects at %s", str(coords))

            if len(coords) != 3:
                pass
                # print("Invalid number of line points:", coords, "\t Mode:", mode)
            if mode == 1 or mode == 2 or mode == 4:
                linelist.append(coords)

    print("Found", len(linelist), "lines.")
    return linelist
# End of function layer()


def intersect(linepoints, depth):
    """
    Take a pair of points and find their intersection with the slice

    @param linepoints:  pair of points
    @param depth:       depth of slice
    """
    logging.debug("The points to interpolate: %s", str(linepoints))
    X = linepoints[0][:]
    N = [0, 0, 1]  # normal to z plane
    V = [0, 0, 0]
    for i in range(3):
        V[i] = linepoints[0][i] - linepoints[1][i]
    logging.debug("V = %s", str(V))

    W = [x - y for x, y in zip(X, [0, 0, depth])]

    dot = lambda a, b: sum(i * j for (i, j) in zip(a, b))
    k = (dot(W, N)) / (dot(V, N))

    I = [x * k for x in V]
    I = [x - y for x, y in zip(X, I)]

    if I[2] != depth:
        logging.debug("Intersection not on slice plane! %s", str(I))
        # return 1

    logging.debug("Intersection at %s", str(I))

    return tuple(I[0:2])
# End of function intersect()


