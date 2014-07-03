"""
Created by Jon Elmer on 01-07-2014
"""

from tkinter import *       # GUI

def load_STL_ASCII (fileName, sliceDepth):
    """Load a facet from an STL file"""

    pointsList = []

    file = open(fileName, "r")

    line = file.readlines(1)[0]
    
    if line.startswith("solid"):
        #ASCII file
        print("Looks like an ASCII file")
        
    else:
        print("Bad File")
        return 1

    for line in file:
    
        line = line.rstrip().lstrip()
        #print(line)

        if line.startswith("facet normal "):
            # Start of a facet
            normal = [0, 0, 0]

            #print("load the normal")
            line = line.lstrip("facet normal ")
            for i, val in enumerate(line.split()):
                try:
                    normal[i] = float(val)
                    #print(float(val), "is float number ", i)
                    
                except:
                    print(val, "is not a float")
               
            #Find the coords
            coords = []
            line = file.readline().rstrip().lstrip()

            if  line == "outer loop":
                for i in range(3):
                    line = file.readline().rstrip().lstrip()
                    #print(line)

                    if line.startswith("vertex "):
                        line = line.lstrip("vertex ")
                        point = ()
                        for val in line.split():
                            try:
                                point = point + (float(val),)
                                #print(float(val), "is float number ", j)
                    
                            except ValueError:
                                print(val, "is not a float")
                        coords.append(point)

                    else:
                        print("File is bad - expected vertex")
                        return 1
                    
                # check if the closing lines are right
                line = file.readline().rstrip().lstrip()
                if line != "endloop":
                    print("File is bad - expected endloop")
                    return 1

                line = file.readline().rstrip().lstrip()
                if line != "endfacet":
                    print("File is bad - expected endfacet")
                    return 1

                # if we are still in the loop, we have the facet data so process here

                print("Facet loaded with normal", normal, "\n\tand coords", coords)

                facetPoints = slice_facet(coords, normal, sliceDepth)

                print("Slicer retuned:", facetPoints)

                try:
                    list(facetPoints)
                    pointsList.extend(facetPoints)
                except TypeError:
                    print("No points")

                print("\n--------------------")

                
            else:
                print("File is bad - expected outer loop")
                return 1
            
        elif line == "endsolid":
            # end of file - stop here
            file.close()
            try:
                pointsSet = list(set(pointsList))
                print("Set of points:", pointsSet)
                return pointsSet
            
            except:
                print("List of points:", pointsList)
                return pointsList
            
        else:
            print("File is bad - expected facet normal")
            return 1

        #file.read() #should drop out of for loop as EOF

    file.close()
    print("Maybe file is binary?")
    return 1
# End of function load_STL_ASCII


def slice_facet(facetPoints, facetNormal, sliceDepth):
    """Slice a facet from an STL file to find points that intersect the slice plane"""
 
    # find whether the facet intersects the slice
    touch = [0, 0, 0]
    above = [0, 0, 0]
    below = [0, 0, 0]
    
    for i, point in enumerate(facetPoints):
        if point[2] == sliceDepth:
            touch[i] = 1
            #print("Point", i, "intesects slice")
        elif point[2] > sliceDepth:
            above[i] = 1
            #print ("Point", i, "is above slice")
        elif point[2] < sliceDepth:
            below[i] = 1
            #print ("Point", i, "is below slice")
    print("Above:", sum(above), "\tTouching:", sum(touch), "\tBelow:", sum(below))

    # Find intersections
    coords = []
    
    if (sum(above) == 3) or (sum(below) == 3):      # points are all above or all below
        print ("Facet does not intersect plane")
        return 0
    else:
        print ("Facet intersects plane")
        if sum(touch) == 3:
            # all on the plane - ignore it as all points will be duplicated elsewhere
            pass
            return 0
                    
        elif sum(touch) == 1 and sum(above) == 1 and sum(below) == 1:
            # need to find one intersection
            linePoints = facetPoints[:]
            linePoints.pop(touch.index(1)) #remove the touching point from the list
            
            coords.append(find_intersection(linePoints, sliceDepth))
            
        elif sum(touch) == 1:
            coords.append(tuple(facetPoints[i][0:2]))
            coords.append(coords[0])
            # weve already done this point as only one intersection!

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

        #print("Facet intersects at:", coords)
        return coords
        
    return 1 # dropped out of the loop somewhere??
    
# End of function slice_facet



def find_intersection(linePoints, sliceDepth):
    """Take a pair of points and find their intersection with the slice"""
    print("The points to interpolate:", linePoints)
    X = linePoints[0][:]
    N = [0, 0, 1]   # normal to z plane
    V = [0, 0, 0]
    for i in range(3):
        V[i] = linePoints[0][i] - linePoints[1][i]
    print("V =", V)

    W = [x-y for x,y in zip(X, [0, 0, sliceDepth])]

    k = (dot(W,N))/(dot(V,N))
    print(k)

    I = [x*k for x in V]
    I = [x-y for x,y in zip(X,I)]

    if I[2] != sliceDepth:
        print("Intersection not on slice plane! - But it might be close...", I)
        #return 1

    print("Intersection at", I, "\n")
    
    return tuple(I[0:2])
# End of function find_intersection


def dot(a, b):
    return sum(i*j for (i,j) in zip(a,b))


def plot(pointsList, scale = 10, margin = 5):
    
    root = Tk()
    root.title("Plot of points")

    try:
        canvas = Canvas(root, width=500, height=500, bg = "white")
        canvas.pack()

        for point in pointsList:
            x = (point[0] * scale) + margin
            y = (point[1] * scale) + margin
            canvas.create_oval(x-1,y-1,x+1,y+1,width=1, fill="black")
 
    except:
        print ("An error has occured!")

    root.mainloop()
    

def main():

    #print(find_intersection([[0,0,0],[2,2,2]],1))

    
    plot(load_STL_ASCII("2cm Cube ASCII.STL", 10))
 
    
main()
    
