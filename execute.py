import logging
from decimal import Decimal
from Load import stl
from Load import parameters
from Slicer import slice
from Slicer import sort
from Output import export
from Output import plotter
from Path import perimeter
import filler

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

import os, sys

sys.path.insert(0, os.getcwd())

params = parameters.load("Config.txt")
print(params)

loaded = stl.load(parameters.get(params, "part_file"))
print("Found", len(loaded), "facets")
# print("Loaded: ", loaded)

snapped = slice.snap(loaded)
# print("Snapped:", snapped)

export.csv_header(parameters.get(params, "output_file"))

start = parameters.get(params, "slice_start")
stop = parameters.get(params, "slice_stop")
step = parameters.get(params, "slice_step")
zrange = int((stop - start) / step) + 1

for z in range(0, zrange):
    z = Decimal(z * step + start)

    sliced = slice.snap(slice.layer(snapped[:], z))
    #print("Slicing at", z, sliced)

    if len(sliced) > 0:
        islands = sort.chop(sliced[:])
        #print("Islands:", islands)

        graph = plotter.graph()

        #plotter.points(graph, sliced, 6, "purple")
        #plotter.plot(graph, sliced)

        filllayer = []

        for i, island in enumerate(islands):
            island = sort.merge(sort.clockwise(island))
            islands[i] = island

            plotter.plot(graph, island, 0, "red")

            nozzle = parameters.get(params, "nozzle_dia")

            trimmed = perimeter.trim(perimeter.offset(island, nozzle / 2))
            for p in range(int(parameters.get(params, "perim_count"))):
                if not sort.isclockwise(trimmed[0]):
                    break
                plotter.plot(graph, trimmed)
                trimmed = perimeter.trim(perimeter.offset(trimmed, nozzle))

            plotter.plot(graph, trimmed, 0, "red")
            filllayer.extend(trimmed)


        #export.csv_islands(filename, islands, z)

        plotter.plot(graph, filler.fill(filllayer, parameters.get(params, "fill_spacing"),
                                        parameters.get(params, "fill_angle")), 4, "blue", "black")


    else:
        print("Didn't find any intersections")

graph.mainloop()