import timeit
import logging
from decimal import Decimal
from Load import stl
from Load import parameters
from Slicer import slice
from Slicer import sort
from Output import post
from Output import plotter
from Path import perimeter
import filler
from shapely import geometry

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

import os, sys

sys.path.insert(0, os.getcwd())

def main():
    params = parameters.load("Config.txt")
    print(params)

    loaded = stl.load(parameters.get(params, "part_file"))
    print("Found", len(loaded), "facets")
    # print("Loaded: ", loaded)

    snapped = slice.snap(loaded)
    # print("Snapped:", snapped)

    plotterscale = parameters.get(params, "plotter_scale")

    nozzle = parameters.get(params, "nozzle_dia")
    perim_count = int(parameters.get(params, "perim_count"))

    output_file = parameters.get(params, "output_file")
    post.newfile(output_file)

    start = parameters.get(params, "slice_start")
    stop = parameters.get(params, "slice_stop")
    step = parameters.get(params, "slice_step")
    zrange = int((stop - start) / step) + 1

    slices = []
    for z in range(0, zrange):
        slices.append(Decimal(z * step + start))

    graph = []
    for z in slices:

        print("Slicing at", z)
        sliced = slice.layer(snapped[:], z)

        # Plot the raw data:
        #g = plotter.graph("RAW", scale=plotterscale)
        #plotter.plot(g, sliced)

        if len(sliced) == 0:
            z += Decimal("0.01")
            for i, s in enumerate(slices):
                slices[i] = s + Decimal("0.01")
            sliced = slice.layer(snapped[:], z)

        sliced = slice.snap(sliced)
        #print("Slicing at", z, sliced)

        if len(sliced) > 0:
            islands = sort.chop(sliced[:])
            if len(islands) > 0:
                g = plotter.graph("Z = {}".format(z), scale=plotterscale)
                graph.append(g)

                print("Found", len(islands), "islands to fill")
                for i, island in enumerate(islands):
                    islands[i] = sort.merge(island)
                    #plotter.plot(g, island, "green")

                merged = perimeter.polygon(sort.clockwise(islands[0]))
                print(merged.area)

                for i, island in enumerate(islands[1:]):
                    try:
                        mergee = perimeter.polygon(sort.clockwise(island))
                        print(mergee.geom_type)
                        merged = perimeter.merge(merged, mergee)
                    except:
                        print("Unable to merge", i)


                print("Merged:", merged.geom_type)
                if merged.geom_type == "Polygon":
                    print("Polygons: 1")
                else:
                    print("Polygons:", len(merged.geoms))
                #print("Islands:", islands)

                #merged = merged[:]


                plotter.plot(g, perimeter.linepoly(merged), "--red")

                filllayer = []

                # Generate perimeter scans
                for p in range(0, perim_count + 1):

                    o = Decimal(p + 0.5) * nozzle

                    offset = perimeter.offset(merged, o)

                    fillarea = True

                    if p < perim_count:
                        # Perimeter scans:
                        plotter.plot(g, perimeter.linepoly(offset), "black", "", scale=plotterscale)

                        post.path(output_file, perimeter.linepoly(offset))

                    filllayer = (perimeter.linepoly(offset))
                    #print("Lines bounding fill:", len(filllayer))


                if fillarea:
                    print("Filling layer...")

                    #print(filllayer)

                    fill = filler.fill(filllayer, parameters.get(params, "fill_spacing"), parameters.get(params, "fill_angle"))


                    for f in fill:
                        plotter.plot(g, f, "blue", "", 0, scale=plotterscale)

                        post.path(output_file, f)

                post.endlayer(output_file)

        else:
            print("Didn't find any intersections")
    return

print("Processing took:", timeit.timeit(main, number=1), "seconds")


plotter.graph(scale=800)
plotter.graph(scale=800).mainloop()
#graph[0].mainloop()