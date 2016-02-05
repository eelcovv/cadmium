#!/usr/bin/python

import sys
import math

from cadmium import *

try:
    stlfname = sys.argv[1]
except IndexError:
    from os.path import basename, splitext
    stlfname = splitext(basename(__file__))[0] + ".stl"

c0 = Cylinder(radius=1, height=8, center=True)
c1 = Cylinder(radius=1, height=8, center=True).rotate(X_axis, 45)
c2 = Cylinder(radius=1, height=8, center=True).rotate(X_axis, -45)
c3 = Cylinder(radius=1, height=8, center=True).rotate(X_axis, 90)
b = Box(x=8,y=1,z=1,center=True)
s0 = Sphere(r=1).translate(1.5,0,0)
s1 = Sphere(r=1).translate(-1.5,0,0)

u = ((c0 + c1 + c2 + c3) - b) - (s0 + s1)

u.toSTL(stlfname)
