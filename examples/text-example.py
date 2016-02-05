
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

s = Text('Cadmium',
  fontpath='DejaVuSerif.ttf', # Give full path on your system
  height=5,
  thickness=2)

s.toSTL(stlfname)
