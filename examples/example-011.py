#!/usr/bin/python
# this example does not work

import os
import sys
import math
sys.path.append('./src')

from cadmium import *

try:
    jsonfname = sys.argv[1]
except IndexError:
    from os.path import basename, splitext
    jsonfname = splitext(basename(__file__))[0] + ".json"

t = Torus(r1=10,r2=2)

precision = 0.01
t.toJSON(jsonfname,compress=True,precision=precision)
size = os.stat(jsonfname).st_size
print size,precision

while size > 40*1024 and precision <= 0.1: # 40k
  os.remove(jsonfname)

  precision += 0.01
  t = Torus(r1=10,r2=2)
  t.toJSON(jsonfname)

  size = os.stat(jsonfname).st_size
  print size,precision
  

