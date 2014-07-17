import logging
from decimal import Decimal
from STL_Loader import stl
from Slicer import slice
from Slicer import sort
from Output import export
from Output import plotter
from Path import perimeter

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.WARNING)

loaded = stl.load("Parts\\2cm Cube Binary.STL")
print("Found", len(loaded), "facets")
print("Loaded: ", loaded)

snapped = slice.snap(loaded)
print("Snapped:", [snap[1:] for snap in snapped])

sliced = slice.snap(slice.layer(snapped[:], Decimal(1)))
print("Sliced: ", sliced)

islands = sort.chop(sliced[:])
print("Islands:", islands)

graph = plotter.graph()

#plotter.points(graph, sliced, 6, "purple")

for island in islands:
    island = sort.clockwise(island)
    export.csv(island, "test.csv")

    plotter.plot(graph, sort.splice(island, 0))

    offset = perimeter.offset(island, 1)
    #plotter.plot(graph, offset)

    trimmed = perimeter.trim(offset)
    plotter.plot(graph, trimmed)

graph.mainloop()