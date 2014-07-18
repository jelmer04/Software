import logging
from decimal import Decimal
from STL_Loader import stl
from Slicer import slice
from Slicer import sort
from Output import export
from Output import plotter
from Path import perimeter

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)

loaded = stl.load("Parts\\Graham\\Pyramid02_with_internal_rogue_triangle.stl")
print("Found", len(loaded), "facets")
print("Loaded: ", loaded)

snapped = slice.snap(loaded)
print("Snapped:", snapped)

filename = "Parts\\Graham\\Pyramid02.csv"
export.csv_header(filename)

thickness = 0.5
height = 5

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

            plotter.plot(graph, sort.splice(island, 1))

            #offset = perimeter.offset(island, 1)
            #plotter.plot(graph, offset)

            #trimmed = perimeter.trim(offset)
            #plotter.plot(graph, trimmed)

        export.csv_islands(filename, islands, z)

        graph.mainloop()
    else:
        print("Didn't find any intersections")

