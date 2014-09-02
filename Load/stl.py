import struct           # Byte manipulation
import os               # File size
import logging          # Message logging


def type(filename):
    """
    Return the type (ASCII or Binary) of the specified STL file.

    Other = 0, ASCII = 1, Binary = 2

    @type  filename:    string
    @param filename:    path of the STL file
    @rtype:         number
    @return:        the type of file
    """
    # Open the file for binary reading
    file = open(filename, "br")
    # Skip the header
    file.seek(80)
    # Read the 4 byte unsigned long for the number of facets in the solid and convert to unsigned integer
    facetcount = struct.unpack('<I', file.read(4))[0]
    # Estimate the size of the file (50 bytes per facet, plus 80 header and 4 facet count)
    estimateSize = 84 + (facetcount * 50)
    # Get the number of bytes in the file
    filesize = os.path.getsize(filename)
    # Log the file size comparison
    logging.info("File should contain   %d facets", facetcount)
    logging.info("File size should be   %d bytes", estimateSize)
    logging.info("File size is actually %d bytes", filesize)
    # Close the file, we're done with it for now
    file.close()
    # Check the size of the file is as expected for the number of facets
    if filesize == estimateSize:
        # It's a binary file
        return 2
    else:
        # Read the first and last lines of the file
        file = open(filename, "r")
        firstline = file.readlines(1)[0]
        for lastline in file:
            pass
        # Close the file, we're done with it now
        file.close()
        # Check if the file is formatted as expected
        if firstline.startswith("solid") and lastline.startswith("endsolid"):
            # It's an ASCII file
            return 1
        else:
            # It's not an STL file
            return 0
# End of function type()


def load_ASCII(filename):
    """
    Load facets and normals from an ASCII formatted STL file.

    Returns a list of facets in the format [(i, j, k), (x, y, z), (x, y, z), (x, y, z)]...

    @type  filename:    string
    @param filename:    path of the STL file
    @rtype:             list
    @return:            list of facets [(normal), (point), (point), (point)]...
    """
    # Open the file in ASCII mode
    with open(filename, "r") as file:
        # List of points which make up each facet
        facetlist = []
        # Read the first line and check if it says solid
        line = file.readlines(1)[0]
        if line.startswith("solid"):
            # Loop through the entire file, loading in facets
            for line in file:
                # Clear out the whitespace
                line = line.rstrip().lstrip()
                # If its the start of a facet:
                if line.startswith("facet normal "):
                    # Find the normal:
                    normal = ()
                    line = line.lstrip("facet normal ")
                    for i, val in enumerate(line.split()):
                        try:
                            normal += (float(val), )
                        except ValueError:
                            logging.debug("%s is not a float", val)
                            return 1

                    # Find the coords:
                    coords = [normal]
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
                        if line == "endloop":
                            pass

                        else:
                            logging.warning("File is bad - expected endloop")
                            return 1

                        line = file.readline().rstrip().lstrip()
                        if line == "endfacet":
                            logging.debug("Facet loaded with normal %s\tand coords %s", str(normal), str(coords))
                            facetlist.append(coords)

                        else:
                            logging.warning("File is bad - expected endfacet")
                            return 1

                    else:
                        logging.warning("File is bad - expected outer loop")
                        return 1

                elif line.startswith("endsolid"):
                    # end of file - stop here
                    return facetlist
                else:
                    logging.warning("File is bad - expected facet normal")
                    return 1
        else:
            logging.warning("File is bad - expected solid")
            return 1
    logging.warning("Dropped out of the loop - something went wrong!")
    return 1
# End of function load_ASCII()


def load_binary(filename):
    """
    Load facets and normals from a binary formatted STL file.

    Returns a list of facets in the format [(i, j, k), (x, y, z), (x, y, z), (x, y, z)]...

    @type  filename:    string
    @param filename:    path of the STL file
    @rtype:             list
    @return:            list of facets [(normal), (point), (point), (point)]...
    """
    with open(filename, "br") as file:
        # List of points which make up each facet
        facetlist = []
        # Skip the header
        file.seek(80)
        # Number of facets to find
        facetCount = struct.unpack("<I", file.read(4))[0]

        # Loop through the entire file, loading in facets
        for x in range(facetCount):
            # Find the normal:
            normal = ()
            for i in range(3):
                normal += (struct.unpack("<f", file.read(4))[0], )
            logging.debug("Normal is %s", str(normal))

            # Find the coords:
            coords = [normal]
            for i in range(3):
                point = ()
                for j in range(3):
                    point += (struct.unpack("<f", file.read(4))[0], )
                coords.append(point)
            logging.debug("Points are %s", str(coords))

            # Read the attribute byte count
            attribute = struct.unpack("<H", file.read(2))[0]
            if attribute != 0:
                logging.warning("File bad - attribute not zero")
                # Graham's files were non-zero?
                #return 1
            # Got the coordinates
            logging.debug("Facet loaded with normal %s\n\tand coords %s", str(normal), str(coords))
            facetlist.append(coords)
        return facetlist
# End of function load_binary()


def load(filename):
    """
    Automatically load facet data from an STL by detecting type

    @param filename:    STL file to load
    @return:            Facet data from load_ASCII or load_binary
    """
    filetype = type(filename)
    if filetype == 2:
        return load_binary(filename)
    elif filetype == 1:
        return load_ASCII(filename)
    else:
        logging.warning("File is not a valid STL file")
    return
# End of function load()
