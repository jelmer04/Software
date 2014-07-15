import logging

from STL_Loader import stl
from Slicer import slice
from Slicer import sort

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.WARNING)

print(stl.load("Parts\\2cm Cube Binary.STL"))
print(stl.load("Parts\\2cm Cube ASCII.STL"))

sliced = slice.layer(slice.snap(stl.load("Parts\\2cm V.STL")), 15)
print(sliced)
print(sort.chop(sliced))
