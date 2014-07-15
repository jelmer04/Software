import logging

from STL_Loader import stl
from Slicer import slice
from Slicer import sort

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.WARNING)

loaded = stl.load("Parts\\2cm V.STL")
print("Loaded: ", loaded)

snapped = slice.snap(loaded)
print("Snapped:", snapped)

sliced = slice.snap(slice.layer(snapped[:], 15))
print("Sliced: ", sliced)

print(sort.chop(sliced))
