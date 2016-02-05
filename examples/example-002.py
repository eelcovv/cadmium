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

b0 = Box(x=4, y=4, z=4, center=True)
b1 = Box(x=4, y=4, z=4, center=True).rotate(X_axis, 45)
b2 = Box(x=4, y=4, z=4, center=True).rotate(Y_axis, 45)
b3 = Box(x=4, y=4, z=4, center=True).rotate(Z_axis, 45)

p = b0 * b1 * b2 * b3

p.toSTL(stlfname)
