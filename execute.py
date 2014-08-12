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
        sliced = slice.snap(slice.layer(snapped[:], z))
        #print("Slicing at", z, sliced)

        if len(sliced) > 0:
            islands = sort.chop(sliced[:])

            for i, island in enumerate(islands):
                separate = perimeter.separate(island)

                if separate:
                    islands[i] = separate[0]
                    for s in separate[1:]:
                        islands.append(s)

            #print("Islands:", islands)
            print("Found", len(islands), "islands to fill")

            g = plotter.graph("Z = {}".format(z), scale=plotterscale)
            graph.append(g)

            filllayer = []
            for i, island in enumerate(islands):
                island = (sort.clockwise(island[:]))
                #islands[i] = island

                #plotter.plot(g, island, "--red", "")

                # Generate perimeter scans
                if len(island) > 0:
                    for p in range(0, perim_count +1):
                        #if p == 0:
                        #    o = nozzle/2
                        #    offset = island
                        #else:
                        #    o = nozzle

                        o = Decimal(p + 0.5) * nozzle

                        offset = sort.chop(slice.snap(perimeter.offset(island[:], o)))[0]
                        #plotter.plot(g, offset, "", "green", scale=plotterscale)

                        #trimmed = slice.snap(perimeter.trim(offset))
                        #plotter.plot(g, trimmed, "black", "", scale=plotterscale)

                        fillarea = True

                        if p < perim_count:

                            plotter.plot(g, offset, "black", "", scale=plotterscale)

                            post.path(output_file, offset)

#                    offset = offset[len(island):]

                    #plotter.plot(g, offset, "--red", "", scale=plotterscale)

                    #print("Island fill:", offset)

                    filllayer.extend(offset)


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


#plotter.graph(scale=800)
plotter.graph(scale=800).mainloop()
#graph[0].mainloop()