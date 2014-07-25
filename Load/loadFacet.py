"""
Created by Jon Elmer on 01-07-2014


"""

from tkinter import *  # GUI
import struct  # Byte manipulation
import os  # File size
import logging
import collections
import math


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


def load_STL(fileName):
    """Load the STL file, either ASCII or Binary - detected automatically"""

    # Open the file for binary reading
    file = open(fileName, "br")
    # Skip the header
    file.seek(80)
    # Read the 4 byte unsigned long for the number of facets in the solid and convert to unsigned integer
    facetCount = struct.unpack('<I', file.read(4))[0]
    # Estimate the size of the file (50 bytes per facet, plus 80 header and 4 facet count)
    estimateSize = 84 + (facetCount * 50)
    # Get the number of bytes in the file
    fileSize = os.path.getsize(fileName)
    # Print the file size comparison
    logging.info("File should contain   %d facets", facetCount)
    logging.info("File size should be   %d bytes", estimateSize)
    logging.info("File size is actually %d bytes", fileSize, )
    file.close()
    # Check the size of the file is as expected for the number of facets
    if fileSize == estimateSize:
        # Its a binary file
        print("Opening", fileName, "in binary mode...")
        file = open(fileName, "br")
        output = load_STL_binary(file)
        file.close()
    else:
        # Its an ASCII file
        print("Opening", fileName, "in ASCII mode...")
        file = open(fileName, "r")
        output = load_STL_ASCII(file)
        file.close()
    return output


# End of function load_STL


def load_STL_ASCII(file):
    """Load a facet from an STL file"""

    # List of points which make up each facet
    facetList = []
    normalsList = []
    # Read the first line and check if it says solid
    line = file.readlines(1)[0]
    if not line.startswith("solid"):
        logging.warning("File is bad - expected solid")
        return 1
    # Loop through the entire file, loading in facets
    for line in file:
        # Clear out the whitespace
        line = line.rstrip().lstrip()
        # If its the start of a facet:
        if line.startswith("facet normal "):
            # Find the normal:
            normal = [0, 0, 0]
            line = line.lstrip("facet normal ")
            for i, val in enumerate(line.split()):
                try:
                    normal[i] = float(val)
                except ValueError:
                    logging.debug("%s is not a float", val)
                    return 1
            normalsList.append(normal)

            # Find the coords:
            coords = []
            line = file.readline().rstrip().lstrip()
            if line == "outer loop":
                for i in range(3):
                    line = file.readline().rstrip().lstrip()
                    if line.startswith("vertex "):
                        line = line.lstrip("vertex ")
                        point = ()
                        for val in line.split():
                            try:
                                point = point + (float(val),)
                            except ValueError:
                                logging.debug("%s is not a float", val)
                        coords.append(point)
                    else:
                        logging.warning("File is bad - expected vertex")
                        return 1

                # Check if the closing lines of each facet are correct
                line = file.readline().rstrip().lstrip()
                if line != "endloop":
                    logging.warning("File is bad - expected endloop")
                    return 1

                line = file.readline().rstrip().lstrip()
                if line != "endfacet":
                    logging.warning("File is bad - expected endfacet")
                    return 1

                # if we are still in the loop, we have the facet data so process here

                logging.debug("Facet loaded with normal %s\tand coords %s", str(normal), str(coords))
                facetList.append(coords)

            else:
                logging.warning("File is bad - expected outer loop")
                return 1

        elif line == "endsolid":
            # end of file - stop here
            return zip(facetList, normalsList)
        else:
            logging.warning("File is bad - expected facet normal")
            return 1
    logging.warning("Dropped out of the loop - something went wrong!")
    return 1


# End of function load_STL_ASCII


def load_STL_binary(file):
    """Load a facet from an STL file"""

    normalsList = []
    # List of points which make up each facet
    facetList = []
    # Read the 80 byte ASCII header
    header = struct.unpack("80s", file.read(80))[0].decode("utf-8").rstrip()
    logging.debug("File Header: %s", header)
    # Number of facets to find
    facetCount = struct.unpack("<I", file.read(4))[0]

    # Loop through the entire file, loading in facets
    for x in range(facetCount):
        # Find the normal:
        normal = [0, 0, 0]
        for i in range(3):
            normal[i] = struct.unpack("<f", file.read(4))[0]
        normalsList.append(normal)

        # Find the coords:
        coords = [0, 0, 0]
        for i in range(3):
            point = ()
            for j in range(3):
                point = point + (struct.unpack("<f", file.read(4))[0],)
            coords[i] = point

        # Read the attribute byte count
        attribute = struct.unpack("<H", file.read(2))[0]
        if attribute != 0:
            logging.warning("File bad - attribute not zero")
            return 1
        # Got the coordinates
        logging.debug("Facet loaded with normal %s\n\tand coords %s", str(normal), str(coords))
        facetList.append(coords)
    return zip(facetList, normalsList)
# End of function load_STL_binary


def slice_facet(facetPoints, sliceDepth):
    """Slice a facet from an STL file to find points that intersect the slice plane"""

    # find whether the facet intersects the slice
    touch = [0, 0, 0]
    above = [0, 0, 0]
    below = [0, 0, 0]

    for i, point in enumerate(facetPoints):
        if point[2] == sliceDepth:
            touch[i] = 1
        elif point[2] > sliceDepth:
            above[i] = 1
        elif point[2] < sliceDepth:
            below[i] = 1
    logging.debug("Above: %d\tTouching: %d\tBelow: %d", sum(above), sum(touch), sum(below))

    # Find intersections
    coords = []
    mode = 0

    if (sum(above) == 3) or (sum(below) == 3):  # points are all above or all below
        logging.debug("Facet does not intersect plane")
        return 0
    else:
        logging.debug("Facet intersects plane")
        if sum(touch) == 3:  # MODE 5
            mode = 5
            # all on the plane - ignore it as all points will be duplicated elsewhere
            pass
            return 0

        elif sum(touch) == 1:
            if sum(above) == 1 and sum(below) == 1:  # MODE 2
                mode = 2
                # need to find one intersection
                linePoints = facetPoints[:]
                touching = linePoints.pop(touch.index(1))[0:2]
                coords.append(touching)  # remove the touching point from the list
                coords.append(find_slice_intersection(linePoints, sliceDepth))
                pass

            elif sum(above) == 0 or sum(below) == 0:  # MODE 3
                mode = 3
                coords.append(tuple(facetPoints[i][0:2]))
                coords.append(coords[0])
                # already done this point as only one intersection!
                return 0

        elif sum(touch) == 2:  # MODE 4
            mode = 4
            coords = facetPoints[:]
            coords.pop(touch.index(0))
            coords = [tuple(coords[0][0:2]), tuple(coords[1][0:2])]

        elif sum(above) == 2 or sum(below) == 2:  # MODE 1
            mode = 1
            if sum(above) == 2:
                pair = above[:]
            else:
                pair = below[:]

            linePoints = facetPoints[:]
            linePoints.pop(pair.index(1))

            coords.append(find_slice_intersection(linePoints, sliceDepth))

            linePoints = facetPoints[:]
            linePoints.reverse()
            pairReversed = pair[:]
            pairReversed.reverse()
            linePoints.pop(pairReversed.index(1))

            coords.append(find_slice_intersection(linePoints, sliceDepth))

    logging.debug("Facet intersects at %s", str(coords))

    if len(coords) is 1:
        print("Only one coord:", coords, "\t Mode:", mode)

    return coords


# End of function slice_facet


def find_slice_intersection(linePoints, sliceDepth):
    """Take a pair of points and find their intersection with the slice"""
    logging.debug("The points to interpolate: %s", str(linePoints))
    X = linePoints[0][:]
    N = [0, 0, 1]  # normal to z plane
    V = [0, 0, 0]
    for i in range(3):
        V[i] = linePoints[0][i] - linePoints[1][i]
    logging.debug("V = %s", str(V))

    W = [x - y for x, y in zip(X, [0, 0, sliceDepth])]

    k = (dot(W, N)) / (dot(V, N))

    I = [x * k for x in V]
    I = [x - y for x, y in zip(X, I)]

    if I[2] != sliceDepth:
        logging.debug("Intersection not on slice plane! %s", str(I))
        # return 1

    logging.debug("Intersection at %s", str(I))

    return tuple(I[0:2])


# End of function find_intersection


def order_points_by_distance(points):
    sortedPoints = []

    # Find vectors from first point to all others
    vectors = []
    startPoint = (0, 0)
    for point in points:
        vector = ((point[0] - startPoint[0]), (point[1] - startPoint[1]))
        vectors.append(vector)

    vector = (0, 0)

    while 0 < len(vectors):
        distances = [find_length((v[0] - vector[0], v[1] - vector[1])) for v in vectors]
        closestIndex = distances.index(min(distances))
        closestPoint = points[closestIndex]
        logging.debug("Distance from %s\tto %s\tis %s\tClosest point: %s", str(vector), str(vectors), str(distances),
                      str(closestPoint))
        sortedPoints.append(points.pop(closestIndex))
        vector = vectors.pop(closestIndex)

    logging.debug("In order: %s", str(sortedPoints))

    return sortedPoints


# End of function order_points_by_distance


def flatten(l):
    return [item for sublist in l for item in sublist]


def next_point_by_distance(startPoint, points):
    # Find vectors from first point to all others
    vectors = []
    # print(points)
    for p in points:
        #print(p)
        vectors.append(tuple((p[0] - startPoint[0], p[1] - startPoint[1])))
    # Start from the first point

    distances = [find_length(v) for v in vectors]
    closestIndex = distances.index(min(distances))
    closestPoint = points[closestIndex]
    logging.debug("Distance from %s\tto %s\tis %s\tClosest point: %s", str(startPoint), str(vectors), str(distances),
                  str(closestPoint))
    return closestIndex


# End of function next_point_by_distance


def order_points_in_pairs(points, normals):
    '''maxValue = 0
    # Find a suitable rounding value
    for (a, b) in points:
        maxValue = max(a[0], a[1], b[0], b[1], maxValue)

    exponent = int(float.hex(maxValue).split("p")[1])
    precision = int(math.log10(2 ** (23 - exponent)))
    logging.debug("Max:", maxValue, "Exponent:", exponent, "Precision:", precision)
    rounding = precision - 1
    logging.debug("Rounding to:", rounding)'''

    sortedPoints = []
    sortedNormals = []
    loops = []
    rounding = 5

    # Round the points for better searching
    roundedPoints = []
    for i, p in enumerate(points):
        try:
            (a, b) = p
            # print("P=", a, "\t", b)
            roundedPoints.append(
                [(round(a[0], rounding), round(a[1], rounding)), (round(b[0], rounding), round(b[1], rounding))])
            #print(p)
        except ValueError:
            print("Error on", i, "\t Data:", p)

    # Start from origin
    nextPoint = (0, 0)
    nextRound = (0, 0)

    while 0 < len(points):
        logging.debug("At: $s", str(nextPoint))
        try:
            nextIndex = flatten(roundedPoints).index(nextRound)

        except ValueError:
            # print("Couldn't find %s in %s"%(str(nextPoint),str(points)))
            #nextIndex = next_point_by_distance(nextRound, flatten(roundedPoints))
            nextIndex = next_point_by_distance(nextPoint, flatten(points))

            if len(sortedPoints) > 0:
                #print("Splitting loop at", nextPoint)
                #print("A loop:", sortedPoints)
                sortedPoints.append(nextPoint)  # Close the loop
                loops.append(sortedPoints)
                sortedPoints = []
                #sortedPoints = [flatten(points)[nextIndex]]

        sortedNormals.append(normals.pop(nextIndex))

        pairOffset = nextIndex % 2
        nextIndex = int((nextIndex - pairOffset) / 2)

        # print("Next index: %d \t Pair offset: %d"%(nextIndex,  pairOffset))
        #print("Length: ", len(points), "\t Point:", points[nextIndex])
        #print("Next closest: %s"%str(points[nextIndex][pairOffset]))

        line = points.pop(nextIndex)
        roundLine = roundedPoints.pop(nextIndex)

        sortedPoints.append(line[pairOffset])

        if pairOffset:
            # on an odd index - must be the element before next
            nextPoint = line[0]
            nextRound = roundLine[0]
        else:
            # on an even index - must be the following element next
            nextPoint = line[1]
            nextRound = roundLine[1]


            #print("At: %s \tGoing to: %s"%(str(sortedPoints[len(sortedPoints)-1]), str(nextPoint)))
            #print()

    sortedPoints.append(sortedPoints[0])
    loops.append(sortedPoints)
    return (loops, normals)


# End of function order_points_in_pairs


def find_length(vector):
    """ Find length of a vector """
    return ((vector[0]) ** 2 + (vector[1]) ** 2) ** 0.5


def dot(a, b):
    """ Find dot product of vectors """
    return sum(i * j for (i, j) in zip(a, b))


def plot(canvas, pointsList, rad=4, traceColor="black", scale=40, margin=10):
    print("Plotting: ", pointsList)

    try:
        scaled = [((point[0] * scale) + margin, 1000 - (point[1] * scale) - margin) for point in pointsList]

        for i, point in enumerate(scaled):
            x = point[0]
            y = point[1]

            if i == 0:
                fill = "green"
                outline = "green"
            elif i == len(scaled) - 1:
                fill = ""
                outline = "red"
            else:
                fill = ""
                outline = "gray"

            canvas.create_oval(x - rad, y - rad, x + rad, y + rad, width=1, fill=fill, outline=outline)

        lines = scaled[:]
        while 1 < len(lines):
            canvas.create_line(lines[0][0], lines[0][1], lines[1][0], lines[1][1], width=1, fill=traceColor)
            lines.pop(0)

    except:
        print("An error has occurred!")


# End of function plot


def remove_duplicates(listA):
    roundA = []
    listB = []
    rounding = 10

    for i, p in enumerate(listA):
        try:
            (a, b) = p
            # print("P=", a, "\t", b)
            roundA.append(
                [(round(a[0], rounding), round(a[1], rounding)), (round(b[0], rounding), round(b[1], rounding))])

            #print(p)
        except ValueError:
            print("Error on", i, "\t Data:", p)

    for a, r in zip(listA, roundA):
        while 1:
            try:
                index = roundA.index(r)
                listA.pop(index)
                roundA.pop(index)
                # print("a:", a)
            except ValueError:
                break
            if a[0] != a[1]:
                listB.append(a)
            else:
                print(p, "is a repeated point")

                # print(len(listA), "values in", "A:", listA)
    return listB[:]


# End function remove_duplicates


def perimeter_offset(points, normals, offset):
    newPoints = []
    lastPoint = points.pop(0)

    # Find the sign to use
    point = points[0]
    vector = sub(point, lastPoint)
    normal = (vector[1], - vector[0])
    normalLength = find_length(normal)
    normal = (n/normalLength for n in normal)     # Unit vector

    offsetVector = tuple(offset * n for n in normal)
    length = find_length(sub(lastPoint, offsetVector))

    print("Point:", point, "Normal:", normalLength, "Length:", length)

    reference = find_offset_reference(points)
    reference = (0,0)

    if find_length(sub(absolute(sub(lastPoint, reference)), offsetVector)) > find_length(sub(lastPoint, reference)):
        sign = 1
    else:
        sign = -1

    print("sign is", sign)

    points.append(points[0])

    while len(points) > 1:
        point = points[0]

        #normal = normals.pop(0)

        vector = sub(point, lastPoint)
        normal = (sign * vector[1], - sign * vector[0])

        length = find_length(normal)

        print("Line:", lastPoint, point, "Normal:", normal, length)

        if length != 0:

            normal = (n / length for n in normal)  # Unit vector

            offsetVector = tuple(offset * n for n in normal)
            newPoints.append([sub(lastPoint, offsetVector), sub(point, offsetVector)])
        else:
            pass
            #print(lastPoint, point)

        lastPoint = points.pop(0)

    #print("Offset to:", newPoints)
    return newPoints


def perimeter_trim(points):
    newPoints = []

    print("Trimming: ", points)

    lastLine = points[-1]
    points.append(points[0])

    while len(points) > 1:
        thisLine = points.pop(0)
        intersection = find_line_intersection(lastLine[0], sub(lastLine[1], lastLine[0]), thisLine[0],
                                              sub(thisLine[1], thisLine[0]))

        # print("Last line:", lastLine, "\t This line:", thisLine, "\t Intersection:", intersection)

        newPoints.append(intersection)
        lastLine = points.pop(0)

    newPoints.append(newPoints[0])

    return newPoints


def sub(A, B):
    return (A[0] - B[0]), (A[1] - B[1])


def find_line_intersection(posA, dirA, posB, dirB):
    # print(posA, dirA, posB, dirB)

    if (dirA[1] == 0 and dirB[1] == 0) or (
                (dirA[1] != 0 and dirB[1] != 0) and (dirA[0] / dirA[1] == dirB[0] / dirB[1])) or (posA == posB):
        return posB

    R = ((posA[0] * dirB[1]) - (posA[1] * dirB[0]) + (posB[1] * dirB[0]) - (posB[0] * dirB[1])) / (
        (dirA[1] * dirB[0]) - (dirA[0] * dirB[1]))

    I = tuple(R * v for v in dirA)
    I = (I[0] + posA[0], I[1] + posA[1])

    return I


def find_offset_reference(points):
    pointSum = [0, 0]
    for p in points:
        pointSum = (pointSum[0] + p[0], pointSum[1] + p[1])

    midPoint = (pointSum[0] / len(points), pointSum[1] / len(points))

    absSum = [0, 0]

    for p in points:
        p = sub(p, midPoint)
        absSum = (absSum[0] + abs(p[0]), absSum[1] + abs(p[1]))

    offsetPoint = (absSum[0] / len(points), absSum[1] / len(points))

    return offsetPoint


def absolute(p):
    return (abs(p[0]), abs(p[1]))


def main():
    # Slicing at meridian - use 0.1 micron offset
    depth = 15
    offset = 1

    facetPoints, facetNormals = zip(*load_STL("..\\Parts\\Conjoined.STL"))

    pointsSet = []
    normals = []
    print("Loaded", len(facetPoints), "facets")
    for (facet, normal) in zip(facetPoints, facetNormals):
        try:
            slice = slice_facet(facet, depth)
            if slice != 0 and slice != []:
                pointsSet.append(slice)
                normals.append(normal[0:2])
                # print("Got slice", slice, "\t from", facet)
        except:
            print("Could not slice facet!!", facet)
            return

    print("All points:    \t", pointsSet)

    # pointsSet = remove_duplicates(pointsSet)
    #print("Unique points: \t", pointsSet)

    print("Sorting...")
    (loops, normals) = order_points_in_pairs(pointsSet, list(facetNormals))

    #loops.reverse()

    #for i, loop in enumerate(loops):
    #print("Ordered loop", i, "is:", loop)

    #print("Centre at", find_offset_reference(flatten(loops)))

    print("Loops:", loops)
    print("Normals:", normals)

    root = Tk()
    root.title("Plot of points")

    canvas = Canvas(root, width=1000, height=1000, bg="white")
    canvas.pack()

    print("Found", len(loops), "loops...")
    for i, loop in enumerate(loops):
        if 1:
            print("Plotting loop", i)
            plot(canvas, loop, 2)
        else:
            pass
        #plot(canvas, flatten(perimeter_offset(loop, offset)), 10)

        offsetLoop = perimeter_offset(loop, normals, offset)
        print("Offset to:", offsetLoop)

        #plot(canvas, flatten(offsetLoop), 10, "green")
        plot(canvas, perimeter_trim(offsetLoop), 1, "blue")

    root.mainloop()


main()