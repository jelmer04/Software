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
        #print("Rotating!")
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
        ##### For debugging
        #if x == int(xmin * 100) + 4 * int(spacing * 100):
        #    break
        #####

        x = slice.snap_number(x / 100)
        mesh.append(x)


    # Crop the mesh to the specified perimeter
    filllist = []
    startindex = []
    stopindex = []
    flip = False
    for seg, segment in enumerate(mesh):
        intersections = []
        segmentfill = []
        for i, line in enumerate(linelist):
            # If the line is coincident with the mesh:
            if line[1][0] == segment:
                intersections.append([line[0], line[1]])
            if line[2][0] == segment:
                intersections.append([line[0], line[2]])


            # If the mesh segment is within the current line's x limits, find the intersection
            if (line[1][0] < segment < line[2][0]) or (line[1][0] > segment > line[2][0]):
                intersection = perimeter.intersect(line[1], sub(line[2], line[1]), (segment, 0), (0, 1))
                if not intersection:
                    intersection = line[1]
                intersections.append([line[0], tuple(slice.snap_number(x) for x in intersection), i])


        # If the mesh segment has intersections with the perimeter:
        if len(intersections) > 0:

            # Sort the intersections into y-order
            intersections.sort(key=lambda x: x[1][1])

            #print("Segment intersects at:", segment, tuple((str(i[1][1]), str(i[0][1])) for i in intersections))

            # Reverse alternate lines to achieve snaking pattern
            if flip:
                intersections.reverse()
            flip = not flip

            # Find the lines which are inside the perimeter (normals are opposite sign)
            last = intersections.pop(0)
            first = True
            stopindex.append(None)
            while len(intersections) > 0:
                intersection = intersections.pop(0)
                #print(last[0][1], intersection[0][1])
                if (last[0][1] > 0 > intersection[0][1] and not flip) or (last[0][1] < 0 < intersection[0][1] and flip):
                        #and (ymin <= intersection[1][1] <= ymax and xmin <= intersection[1][0] <= xmax):


                    # Generate the infill line
                    line = [(), last[1], intersection[1]]

                    if first:
                        startindex.append(last[2])
                        first = False

                    stopindex[-1] = intersection[2]

                    # Short fill filter
                    if abs(line[1][1] - line[2][1]) > short:
                        segmentfill.append(line)

                last = intersection

        if len(segmentfill) > 0:
            #print("Segment:", segmentfill)
            #print("Fill List:", len(filllist), filllist)
            if len(segmentfill) > 0 and len(filllist) > 0:
                if len(filllist[-1]) > 0:
                    # Join segments together
                    ###filllist[-1].append([(), filllist[-1][-1][2], segmentfill[0][1]])

                    if len(startindex) > 1:
                        # Calculate the points to join along
                        join = []
                        limits = (startindex[-1], stopindex[-2])

                        #start = min(limits)
                        #stop = max(limits)
                        if flip:
                            start = limits[0]
                            stop = limits[1]
                        else:
                            start = limits[1]
                            stop = limits[0]

                        #print("Join between:", start, stop)

                        if start > stop:
                            if False and start - stop < 50:
                                for s in linelist[stop:start]:
                                    join.append(s[2])
                            else:
                                for s in linelist[start:]:
                                    pass
                                    if mesh[seg-1] < s[2][0] < segment:
                                        pass
                                        join.append(s[2])

                                for s in linelist[:stop]:
                                    pass
                                    if mesh[seg-1] < s[2][0] < segment:
                                        pass
                                        join.append(s[2])

                        else:
                            for s in linelist[start:stop]:
                                join.append(s[2])

                        if flip:
                            join.reverse()

                        join.insert(0, filllist[-1][-1][2])
                        join.append(segmentfill[0][1])
                        #print("Join between:", join)

                        if len(join) > 5:
                            pass
                            #join = [join[0], join[-1]]

                        # Do the joining
                        for j in range(len(join) - 1):
                            filllist[-1].append([(), join[j], join[j+1]])

                            pass

                    if len(segmentfill) > 1:
                        filllist[-1].append(segmentfill.pop(0))
                        filllist.append([])
                    filllist[-1].extend(segmentfill)
                else:
                    filllist.append(segmentfill)
            else:
                filllist.append(segmentfill)
        else:
            filllist.append([])
            pass
    if angle != 0:
        pass
        #print("Rotating back!")
        for i, f in enumerate(filllist):
            filllist[i] = rotate(f, -angle)
            pass
    return list(slice.snap(fill) for fill in filllist)


def rotate(linelist, angle):
    #point = lambda p, s, c: (p[0] * c - p[1] * s, p[0] * s + p[1] * c)

    angle = math.radians(angle)
    sin = Decimal(math.sin(angle))
    cos = Decimal(math.cos(angle))
    rotated = []
    for line in linelist:
        newline = []
        for l in line:
            if len(l) >= 2:
                newline.append(rotate_point(l, sin, cos))
            else:
                newline.append(tuple())
        rotated.append(newline)

    return rotated


def rotate_point(p, s, c):
    #print(p, s, c)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)