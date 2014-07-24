from decimal import Decimal
from Path import perimeter
from Slicer import slice
import math

def fill(linelist, normal, short=0.1):
    """
    Fill between the lines of linelist in the normal direction, at a spacing of 0.5 along the specified direction

    :param linelist:    List of perimeter lines
    :param spacing:     X-spacing between filler lines
    :return:            Fill path
    """


    direction = slice.snap_point([normal[1], -normal[0]])
    normal = slice.snap_point(normal)

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

    # Generate the list of lines to use as the infill mesh
    mesh = []
    x = xmin
    y = ymin
    if normal[1] != 0:
        while y < ymax:
            mesh.append((xmin, y))
            y += abs(normal[1])
    if normal[0] != 0:
        mesh.reverse()
        while x < xmax:
            mesh.append((x, ymin))
            x += abs(normal[0])

    mesh = list(slice.snap_point(m) for m in mesh)
    print("Mesh:", mesh)

    # Crop the mesh to the specified perimeter
    filllist = []
    flip = False
    for segment in mesh:
        intersections = []
        for i, line in enumerate(linelist):
            intersection = slice.snap_point(perimeter.intersect(line[1], sub(line[2], line[1]), segment, direction))
            #print("Intersects at:", intersection)
            if max(p[0] for p in line[1:]) >= intersection[0] >= min(p[0] for p in line[1:]) \
                    and max(p[1] for p in line[1:]) >= intersection[1] >= min(p[1] for p in line[1:]):
                intersections.append([line[0], intersection])

        #print("Intersections:", intersections)
        # If the mesh segment has intersections with the perimeter:
        if len(intersections) > 0:
            # Sort the intersections into distance order
            intersections.sort(key=lambda i: sum(x ** 2 for x in sub(i[1], segment)))

            #print("Sorted Intersections:", intersections)

            # Reverse alternate segments to achieve snaking pattern
            if flip:
                intersections.reverse()

            flip = not flip

            # Find the lines which are inside the perimeter (normals are opposite sign)
            last = intersections.pop(0)
            anglelast = 180 - angle(last[0][:2], normal[:2])
            while len(intersections) > 0:
                intersection = intersections.pop(0)
                #print("Normals:", intersection[0], last[0])

                angleint = angle(intersection[0][:2], normal[:2])
                #anglelast = angle(last[0][:2], normal[:2])

                if intersection[0][0] * last[0][0] < 0 or intersection[0][1] * last[0][1] < 0:
                #if angleint <= 90 <= anglelast or angleint >= 90 >= anglelast:
                    print("Angles:", angle(last[0][:2], tuple(-n for n in normal[:2])), angle(intersection[0][:2], normal[:2]))
                    # Generate the infill line
                    line = [(), last[1], intersection[1]]

                    # Short fill filter
                    if sum(x ** 2 for x in sub(line[1], line[2])) >= short ** 2:
                        # Join the line to the previous line
                        if len(filllist) > 0:
                            filllist.append([(), filllist[-1][2], line[1]])
                        filllist.append(line)
                last = intersection
                anglelast = 180 - angleint
    return filllist


def angle(a, b):
    return math.degrees(math.acos(dot(a, b)/Decimal(mag(a)*mag(b))))


def sub(x, y):
    return (x[0] - y[0]), (x[1] - y[1])


def dot(a, b):
    return sum(i * j for (i, j) in zip(a, b))


def mag(a):
    return math.sqrt(sum(i ** 2 for i in a))