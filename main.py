import logging
from decimal import Decimal
from STL_Loader import stl
from Slicer import slice
from Slicer import sort
from Output import export
from Output import plotter
from Path import perimeter

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)

<<<<<<< HEAD
<<<<<<< HEAD
import os, sys
sys.path.insert(0, os.getcwd())

loaded = stl.load("Parts\\Graham\\Pyramid01.stl")
=======
loaded = stl.load("Parts\\Graham\\Pyramid02_with_internal_rogue_triangle.stl")
>>>>>>> parent of 0aeef34... Filling along x, merges coincident lines
=======
loaded = stl.load("Parts\\Graham\\Pyramid02_with_internal_rogue_triangle.stl")
>>>>>>> parent of 0aeef34... Filling along x, merges coincident lines
print("Found", len(loaded), "facets")
print("Loaded: ", loaded)

snapped = slice.snap(loaded)
print("Snapped:", snapped)

filename = "Parts\\Graham\\Pyramid02.csv"
export.csv_header(filename)

thickness = 0.5
<<<<<<< HEAD
<<<<<<< HEAD
height = 3
start = 0
=======
height = 5
>>>>>>> parent of 0aeef34... Filling along x, merges coincident lines
=======
height = 5
>>>>>>> parent of 0aeef34... Filling along x, merges coincident lines

for z in range(0, int(height/thickness) + 1):
    z = Decimal(z * thickness)

    print("Snapped:", snapped)

    sliced = slice.snap(slice.layer(snapped[:], z))
    print("Slicing at", z, sliced)

    if len(sliced) > 0:
        islands = sort.chop(sliced[:])
        print("Islands:", islands)

        graph = plotter.graph()

        #plotter.points(graph, sliced, 6, "purple")
        #plotter.plot(graph, sliced)


        for i, island in enumerate(islands):
            island = sort.clockwise(island)
            islands[i] = island
            print("Island:", island)

            plotter.plot(graph, sort.splice(island, 1))

<<<<<<< HEAD
<<<<<<< HEAD
            offset = slice.snap(perimeter.offset(island, Decimal(1)))
            print("Offset to:", offset)

            trimmed = perimeter.trim(offset)
            plotter.plot(graph, trimmed, 2, "red")

            plotter.plot(graph, filler.fill(trimmed, (0.1, 0)), 4, "blue", "black")

=======
            #offset = perimeter.offset(island, 1)
            #plotter.plot(graph, offset)

            #trimmed = perimeter.trim(offset)
            #plotter.plot(graph, trimmed)
>>>>>>> parent of 0aeef34... Filling along x, merges coincident lines
=======
            #offset = perimeter.offset(island, 1)
            #plotter.plot(graph, offset)

            #trimmed = perimeter.trim(offset)
            #plotter.plot(graph, trimmed)
>>>>>>> parent of 0aeef34... Filling along x, merges coincident lines

        export.csv_islands(filename, islands, z)

        graph.mainloop()
    else:
        print("Didn't find any intersections")

