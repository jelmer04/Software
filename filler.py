from Path import perimeter
from Slicer import slice
import math
from decimal import Decimal


def fill(linelist, spacing=0.5, angle=0, short=0.1):
    """
    Fill between the lines of linelist in the y direction, at a spacing of 0.5 along the x direction

    :param linelist:    List of perimeter lines
    :param spacing:     X-spacing between filler lines
    :return:            Fill path
    """
    sub = lambda x, y: ((x[0] - y[0]), (x[1] - y[1]))

    if angle != 0:
        linelist = rotate(linelist, angle)

    # Find the limits
    xmax = linelist[0][1][0]
    xmin = xmax
    ymax = linelist[0][1][1]
    ymin = ymax
    for (n, a, b) in linelist:
        xmax = max((xmax, a[0], b[0]))
        xmin = min((xmin, a[0], b[0]))
        ymax = max((ymax, a[1], b[1]))
        ymin = min((ymin, a[1], b[1]))

    # Generate the list of x lines to use as the infill mesh
    mesh = []
    for x in range(int(xmin * 100), int(xmax * 100) + 1, int(spacing * 100)):
        x = slice.snap_number(x / 100)
        mesh.append(x)

    # Crop the mesh to the specified perimeter
    filllist = []
    flip = False
    for segment in mesh:
        intersections = []
        for i, line in enumerate(linelist):
            # If the mesh segment is within the current line's x limits, find the intersection
            if (line[1][0] < segment < line[2][0]) or (line[1][0] > segment > line[2][0]):
                intersections.append([line[0], tuple(slice.snap_number(x) for x in
                                           perimeter.intersect(line[1], sub(line[2], line[1]),
                                                               (segment, 0), (0, 1)))])
        # If the mesh segment has intersections with the perimeter:
        if len(intersections) > 0:
            # Sort the intersections into y-order
            intersections.sort(key=lambda x: x[1][1])

            # Reverse alternate lines to achieve snaking pattern
            if flip:
                intersections.reverse()
            flip = not flip

            # Find the lines which are inside the perimeter (normals are opposite sign)
            last = intersections.pop(0)
            while len(intersections) > 0:
                intersection = intersections.pop(0)
                if intersection[0][1] * last[0][1] < 0:
                    # Generate the infill line
                    line = [(), last[1], intersection[1]]

                    # Short fill filter
                    if abs(line[1][1] - line[2][1]) > short:
                        if len(filllist) > 0:
                            filllist.append([(), filllist[-1][2], line[1]])
                        filllist.append(line)
                last = intersection

    if angle != 0:
        pass
        filllist = rotate(filllist, -angle)
    return slice.snap(filllist)


def rotate(linelist, angle):
    point = lambda p, s, c: (p[0] * c - p[1] * s, p[0] * s + p[1] * c)

    angle = math.radians(angle)
    sin = Decimal(math.sin(angle))
    cos = Decimal(math.cos(angle))
    rotated = []
    for line in linelist:
        newline = []
        for l in line:
            if len(l) >= 2:
                newline.append(point(l, sin, cos))
            else:
                newline.append(tuple())
        rotated.append(newline)

    return rotated