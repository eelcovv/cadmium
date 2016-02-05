#!/usr/bin/python

import sys
import math
sys.path.append('./src')

from OCC.gp import *

from cadmium import *

try:
    stlfname = sys.argv[1]
except IndexError:
    from os.path import basename, splitext
    stlfname = splitext(basename(__file__))[0] + ".stl"

u = Cylinder(radius=1, height=8, center=True).translate(x=4) + \
  Cylinder(radius=1, height=8, center=True).translate(x=-4)\
    .scale(0.5) + \
  Box(2,2,2, center=True)

u.toSTL(stlfname)
