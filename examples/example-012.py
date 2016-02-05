#!/usr/bin/python

import sys
import math
from cadmium import *

try:
    stlfname = sys.argv[1]
except IndexError:
    from os.path import basename, splitext
    stlfname = splitext(basename(__file__))[0] + ".stl"

s = Sphere(r=3)
s.scale(scaleY=2, scaleZ=2)

s.toSTL(stlfname)
