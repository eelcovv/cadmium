#!/usr/bin/python

import sys
import math
sys.path.append('./src')

from cadmium import *

try:
    stlfname = sys.argv[1]
except IndexError:
    from os.path import basename, splitext
    stlfname = splitext(basename(__file__))[0] + ".stl"

b0 = Box(x=4,y=4,z=4, center=True)
s0 = Sphere(radius=2.5)

u = s0 - b0

u.toSTL(stlfname)
