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

nozzle = parameters.get(params, "nozzle_dia")
perim_count = int(parameters.get(params, "perim_count"))

output_file = parameters.get(params, "output_file")
export.newfile(output_file)

start = parameters.get(params, "slice_start")
stop = parameters.get(params, "slice_stop")
step = parameters.get(params, "slice_step")
zrange = int((stop - start) / step) + 1

graph = []

for z in range(0, zrange):
    z = Decimal(z * step + start)

    export.layer(output_file, z)

    print("Slicing at", z)
    sliced = slice.snap(slice.layer(snapped[:], z))
    #print("Slicing at", z, sliced)

    if len(sliced) > 0:
        islands = sort.chop(sliced[:])
        #print("Islands:", islands)

        g = plotter.graph("Z = {}".format(z))
        graph.append(g)

        #plotter.points(graph, sliced, 6, "purple")
        #plotter.plot(graph, sliced)

        filllayer = []

        for i, island in enumerate(islands):
            island = sort.merge(sort.clockwise(island))
            islands[i] = island

            plotter.plot(g, island, 0, "red")

            if len(island) > 0:
                for p in range(0, perim_count):

                    trimmed = perimeter.offset(island, nozzle * (i + Decimal(0.5)))
                    #trimmed = perimeter.trim(trimmed)

                    if not sort.isclockwise(trimmed[-1]):
                        print("Offset too great")
                        fillarea = False
                    else:
                        fillarea = True
                        plotter.plot(g, trimmed)
                        export.path(output_file, trimmed)


                trimmed = perimeter.offset(island, nozzle * (perim_count))
                #trimmed = perimeter.trim(trimmed)

                plotter.plot(g, trimmed, 0, "red")
                filllayer.extend(trimmed)


            #export.csv_islands(filename, islands, z)
            if fillarea:
                fill = filler.fill(filllayer, parameters.get(params, "fill_spacing"), parameters.get(params, "fill_angle"))

                for f in fill:
                    plotter.plot(g, f, 4, "blue", "black")
                    export.path(output_file, f)


    else:
        print("Didn't find any intersections")

for g in graph:
    g.mainloop()