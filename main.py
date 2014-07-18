import logging
from decimal import Decimal
from STL_Loader import stl
from Slicer import slice
from Slicer import sort
from Output import export
from Output import plotter
from Path import perimeter

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.WARNING)

loaded = stl.load("Parts\\Conjoined 1 Face.STL")
print("Found", len(loaded), "facets")
print("Loaded: ", loaded)

snapped = slice.snap(loaded)
print("Snapped:", [snap[1:] for snap in snapped])

filename = "test.csv"
export.csv_header(filename)

for z in range(0, 1):
    z = slice.snap_number(z/10)
    print("Snapped:", [snap[1:] for snap in snapped])

    sliced = slice.snap(slice.layer(snapped[:], z))
    print("Slicing at", z, sliced)

    if len(sliced) > 0:
        islands = sort.chop(sliced[:])
        print("Islands:", islands)

        graph = plotter.graph()

        #plotter.points(graph, sliced, 6, "purple")
        #plotter.plot(graph, sliced)


        for i, island in enumerate(islands):
            island = slice.snap(sort.clockwise(island))
            islands[i] = island

            plotter.plot(graph, sort.splice(island, 1))

            offset = perimeter.offset(island, 1)
            #plotter.plot(graph, offset)

            trimmed = perimeter.trim(offset)
            plotter.plot(graph, trimmed)

        export.csv_islands(filename, islands, z)

    graph.mainloop()