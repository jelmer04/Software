import logging
from decimal import Decimal
from STL_Loader import stl
from Slicer import slice
from Slicer import sort
from Output import export
from Output import plotter

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.WARNING)

loaded = stl.load("Parts\\2cm V.STL")
print("Loaded: ", loaded)

snapped = slice.snap(loaded)
print("Snapped:", snapped)

sliced = slice.snap(slice.layer(snapped[:], Decimal(15)))
print("Sliced: ", sliced)

islands = sort.chop(sliced)
print("Islands:", islands)

graph = plotter.graph()

for island in islands:
    island = sort.clockwise(island)
    export.csv(island, "test.csv")
    plotter.plot(graph, sort.splice(island, 0))

graph.mainloop()