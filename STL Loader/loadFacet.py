"""
Created by Jon Elmer on 01-07-2014
"""

from tkinter import *  # GUI
import struct  # Byte manipulation
import os  # File size
import logging
import collections
import math


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.WARNING)

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
    logging.info("File size is actually %d bytes", fileSize,)
    file.close()
    # Check the size of the file is as expected for the number of facets
    if fileSize == estimateSize:
        # Its a binary file
        print("Opening", fileName, "in binary mode...")
        file = open(fileName, "br")
        facetList = load_STL_Binary(file)
        file.close()
    else:
        # Its an ASCII file
        print("Opening", fileName, "in ASCII mode...")
        file = open(fileName, "r")
        facetList = load_STL_ASCII(file)
        file.close()
    return facetList
# End of function load_STL


def load_STL_ASCII(file):
    """Load a facet from an STL file"""

    # List of points which make up each facet
    facetList = []
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
            return facetList
        else:
            logging.warning("File is bad - expected facet normal")
            return 1
    logging.warning("Dropped out of the loop - something went wrong!")
    return 1
# End of function load_STL_ASCII


def load_STL_Binary(file):
    """Load a facet from an STL file"""

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
    return facetList
# End of function load_STL_Binary


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

    if (sum(above) == 3) or (sum(below) == 3):  # points are all above or all below
        logging.debug("Facet does not intersect plane")
        return 0
    else:
        logging.debug("Facet intersects plane")
        if sum(touch) == 3:  # MODE 5
            # all on the plane - ignore it as all points will be duplicated elsewhere
            pass
            return 0

        elif sum(touch) == 1:
            if sum(above) == 1 and sum(below) == 1:
                # need to find one intersection
                linePoints = facetPoints[:]
                linePoints.pop(touch.index(1))  # remove the touching point from the list

                coords.append(find_intersection(linePoints, sliceDepth))

            elif sum(above + below) == 0:
                coords.append(tuple(facetPoints[i][0:2]))
                coords.append(coords[0])
                # already done this point as only one intersection!

        elif sum(touch) == 2:
            coords = facetPoints[:]
            coords.pop(touch.index(0))
            coords = [tuple(coords[0][0:2]), tuple(coords[1][0:2])]

        elif sum(above) == 2 or sum(below) == 2:
            if sum(above) == 2:
                pair = above[:]
            else:
                pair = below[:]

            linePoints = facetPoints[:]
            linePoints.pop(pair.index(1))

            coords.append(find_intersection(linePoints, sliceDepth))

            linePoints = facetPoints[:]
            linePoints.reverse()
            pairReversed = pair[:]
            pairReversed.reverse()
            linePoints.pop(pairReversed.index(1))

            coords.append(find_intersection(linePoints, sliceDepth))

    logging.debug("Facet intersects at %s", str(coords))
    return coords
# End of function slice_facet


def find_intersection(linePoints, sliceDepth):
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
        logging.debug("Distance from %s\tto %s\tis %s\tClosest point: %s", str(vector), str(vectors), str(distances), str(closestPoint))
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
    for point in points:
        vector = ((point[0] - startPoint[0]), (point[1] - startPoint[1]))
        vectors.append(vector)
    # Start from the first point

    distances = [find_length((v[0] - startPoint[0], v[1] - startPoint[1])) for v in vectors]
    closestIndex = distances.index(min(distances))
    closestPoint = points[closestIndex]
    logging.debug("Distance from %s\tto %s\tis %s\tClosest point: %s", str(vector), str(vectors), str(distances), str(closestPoint))
    return closestPoint
# End of function next_point_by_distance


def order_points_in_pairs(points):

    #maxValue = 0
    # Find a suitable rounding value
    #for (a, b) in points:
    #    maxValue = max(a, b, maxValue)
    #precision = int(math.log10(2 ** (23-(math.log2(maxValue)))))
    #print("Max:", maxValue, "Precision:", precision)
    #rounding = precision - 1

    sortedPoints = []
    rounding = 5

    # Round the points for better searching
    roundedPoints = []
    for p in points:
        roundedPoints.append([((round(n[0], rounding), round(n[1], rounding)) for n in p)])

    #points = roundedPoints[:]
    #sortedPoints = [(0, 0)]
    #sortedPoints.append(points.pop(0))
    #nextPoint = points.pop(0)
    #roundedPoints.pop(0)
    #nextRound = roundedPoints.pop(0)

    # Start from origin
    nextPoint = (0, 0)
    nextRound = (0, 0)
    while 1 < len(points):


        try:
            nextIndex = roundedPoints.index(nextRound)
        except:
            nextIndex = roundedPoints.index(next_point_by_distance(nextRound, roundedPoints))
            print("Next point not found:", nextPoint, "\tNext closest:", points[nextIndex], "\tAt:", nextIndex)

        sortedPoints.append(points.pop(nextIndex))

        if (nextIndex % 2) == 1:
            # on an odd index - must be the element before next
            #points.pop(nextIndex)
            nextPoint = points.pop(nextIndex - 1)

            roundedPoints.pop(nextIndex)
            nextRound = roundedPoints.pop(nextIndex - 1)
        else:
            # on an even index - must be the following element next
            #points.pop(nextIndex)
            nextPoint = points.pop(nextIndex)

            roundedPoints.pop(nextIndex)
            nextRound = roundedPoints.pop(nextIndex)

        print("At:", str(sortedPoints[len(sortedPoints)-1]), "\tGoing to:", str(nextPoint))

    logging.debug("In order: %s", str(sortedPoints))
    return sortedPoints
# End of function order_points_in_pairs


def find_length(vector):
    """ Find length of a vector """
    return ((vector[0]) ** 2 + (vector[1]) ** 2) ** 0.5


def dot(a, b):
    return sum(i * j for (i, j) in zip(a, b))


def plot(pointsList, scale=40, margin=5, rad = 1.5):
    root = Tk()
    root.title("Plot of points")

    try:
        canvas = Canvas(root, width=1000, height=1000, bg="white")
        canvas.pack()

        scaled = [((point[0] * scale) + margin, 1000 - (point[1] * scale) - margin) for point in pointsList]

        lines = scaled[:]
        while 1 < len(lines):
            canvas.create_line(lines[0][0], lines[0][1], lines[1][0], lines[1][1], width=1, fill='red')
            lines.pop(0)

        for point in scaled:
            x = point[0]
            y = point[1]
            canvas.create_oval(x - rad, y - rad, x + rad, y + rad, width=1, fill="black")

    except:
        print("An error has occurred!")

    root.mainloop()
# End of function plot


def main():
    facetPoints = load_STL("2cm Ball Binary.STL")

    pointsSet = []
    for facet in facetPoints:
        try:
            slice = slice_facet(facet, 2.5)
            if slice != 0:
                pointsSet.append(slice)
        except:
            print("Could not slice facet!!")
    print("All points:    \t", pointsSet)
    #pointsSet = list(set(pointsSet))
    #print("Unique points: \t", pointsSet)
    flatPoints = flatten(pointsSet)
    print("Flat Points:", flatPoints)
    #sortedPoints = order_points_by_distance(flatPoints)
    sortedPoints = order_points_in_pairs(flatten(pointsSet))
    print("Ordered points:\t", sortedPoints)
    plot(sortedPoints)


main()
    
