# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

import fontforge
from OCC.gp import gp_Pnt, gp_Vec
from OCC.TColgp import TColgp_Array1OfPnt
from OCC.Geom import Geom_BezierCurve
from OCC.BRepBuilderAPI import \
  BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse

from cadmium.solid import Solid
import math
INF = math.tan(math.pi/2) # infinity

class Glyph(Solid):
  xmax = -INF
  xmin = INF
  ymax = -INF
  ymin = INF
  zmax = -INF
  zmin = INF
  def __init__(self, char, font, thickness, center=False):
    self.font = font
    self.thickness = thickness
    Solid.__init__(self, self.char_to_solid(char))

    self.xspan = self.xmax - self.xmin
    self.yspan = self.ymax - self.ymin
    if center:
      xmin_target = -(self.xspan/2)
      ymin_target = -(self.yspan/2)
      self.translate(x=(xmin_target-self.xmin), y=(ymin_target-self.ymin))

  def update_extents(self, point):
    self.xmax = max(self.xmax, point.X())
    self.xmin = min(self.xmin, point.X())
    self.ymax = max(self.ymax, point.Y())
    self.ymin = min(self.ymin, point.Y())
    self.zmax = max(self.zmax, point.Z())
    self.zmin = min(self.zmin, point.Z())

  def add_to_wire(self, points, wire):
    array=TColgp_Array1OfPnt(1, len(points))
    for i in range(len(points)):
      array.SetValue(i+1, points[i])
      self.update_extents(points[i])
    curve = Geom_BezierCurve(array)
    me = BRepBuilderAPI_MakeEdge(curve.GetHandle())    
    wire.Add(me.Edge())

  def char_to_solid(self, c):
    glyph = self.font[c]

    self.bbox = glyph.boundingBox()
    self.left_side_bearing = glyph.left_side_bearing
    self.right_side_bearing = glyph.right_side_bearing

    layer = glyph.layers['Fore']
    bodies = []
    
    for contour in layer:
      i = 0
      total = len(contour)
      curve_points = []

      wire = BRepBuilderAPI_MakeWire()
      for point in contour:
        if point.on_curve:
          if i > 0:
            # Complete old curve
            curve_points.append(gp_Pnt(point.x, point.y, 0))
            self.add_to_wire(curve_points, wire)

          if i < total:
            # Start new curve
            curve_points = [gp_Pnt(point.x, point.y, 0)]

          if i == total-1:
            first = contour[0]
            curve_points.append(gp_Pnt(first.x, first.y, 0))
            self.add_to_wire(curve_points, wire)
        else:
          curve_points.append(gp_Pnt(point.x, point.y, 0))
          if i == total-1:
            first = contour[0]
            curve_points.append(gp_Pnt(first.x, first.y, 0))
            self.add_to_wire(curve_points, wire)
        i += 1

      face = BRepBuilderAPI_MakeFace(wire.Wire())
      extrusion_vector = gp_Vec(0, 0, 100)
      prism = BRepPrimAPI_MakePrism(face.Shape(), extrusion_vector)

      bodies.append(dict(
        prism = prism,
        isClockwise = contour.isClockwise(),
      ))

    if len(bodies) > 0:
      if len(bodies) == 1:
        return bodies[0]['prism'].Shape()
      elif len(bodies) > 1:
        final = None
        positive_union = None
        for body in bodies:
          if body['isClockwise'] == 1:
            if positive_union:
              positive_union = BRepAlgoAPI_Fuse(
                positive_union.Shape(), body['prism'].Shape())
            else:
              positive_union = body['prism']

        negative_union = None
        for body in bodies:
          if body['isClockwise'] == 0:
            if negative_union:
              negative_union = BRepAlgoAPI_Fuse(
                negative_union.Shape(), body['prism'].Shape())
            else:
              negative_union = body['prism']
        
        if positive_union and negative_union:
          final = BRepAlgoAPI_Cut(
            positive_union.Shape(), negative_union.Shape())
        elif positive_union:
          final = positive_union
        elif negative_union:
          final = negative_union
        return final.Shape()

class Text(Solid):
  _char_map_ = {
    '!' : 'exclam',
    '"' : 'quotedbl',
    '#' : 'numbersign',
    '$' : 'dollar',
    '%' : 'percent',
    '&' : 'ampersand',
    '\'': 'quotesingle',
    '(' : 'parenleft',
    ')' : 'parenright',
    '*' : 'asterisk',
    '+' : 'plus',
    ',' : 'comma',
    '-' : 'hyphen',
    '.' : 'period',
    '/' : 'slash',
    '0' : 'zero',
    '1' : 'one',
    '2' : 'two',
    '3' : 'three',
    '4' : 'four',
    '5' : 'five',
    '6' : 'six',
    '7' : 'seven',
    '8' : 'eight',
    '9' : 'nine',
    ':' : 'colon',
    ';' : 'semicolon',
    '<' : 'less',
    '=' : 'equal',
    '>' : 'greater',
    '?' : 'question',
    '@' : 'at',
    '[' : 'bracketleft',
    '\\': 'backslash',
    ']' : 'bracketright',
    '^' : 'asciicircum',
    '_' : 'underscore',
    '`' : 'grave',
    '{' : 'braceleft',
    '|' : 'bar',
    '}' : 'braceright',
    '~' : 'asciitilde'
  }
  xmax = -INF
  xmin = INF
  ymax = -INF
  ymin = INF
  zmax = -INF
  zmin = INF

  def merge_extents(self, glyph):
    self.xmax += glyph.left_side_bearing + glyph.xspan +\
      glyph.right_side_bearing
    self.xspan = self.xmax - self.xmin
    self.right_side_bearing = glyph.right_side_bearing
    print 'Merge: ',self.xspan,'[',self.xmin,',',self.xmax,']'

  def init_extents(self, glyph):
    self.xmin = glyph.xmin - glyph.left_side_bearing
    self.xmax = glyph.xmax + glyph.right_side_bearing
    self.xspan = self.xmax - self.xmin
    self.left_side_bearing = glyph.left_side_bearing
    self.right_side_bearing = glyph.right_side_bearing
    print 'Init: ',self.xspan,'[',self.xmin,',',self.xmax,']'

  def centralize(self):
    xmin_target = -(self.xspan/2)
    dx = xmin_target - self.xmin
    print dx
    #self.instance.translate(x=dx)
    #self.xmin = xmin_target
    #self.xmax = self.xmin + self.xspan

  def __init__(self, text, fontpath, thickness=1, center=False):

    font = fontforge.open(fontpath)

    self.instance = None
    for char in text:
      if char >= 'a' and char <= 'z':
        c = char
      elif char >= 'A' and char <= 'Z':
        c = char
      else:
        c = self._char_map_.get(char)
      
      if not c: continue
        
      if self.instance:
        g = Glyph(c, font, thickness, center=True)
        g.translate(x=(self.width+g.left_side_bearing+(g.xspan/2)))
        ymax_target = g.bbox[3]
        g.translate(y=(ymax_target-g.yspan/2))

        self.instance += g
        self.width += g.left_side_bearing+g.xspan+g.right_side_bearing
      else:
        g = Glyph(c, font, thickness, center=True)
        ymax_target = g.bbox[3]
        g.translate(y=(ymax_target-g.yspan/2))
        self.instance = g
        self.width = (g.xspan/2)+g.right_side_bearing

      #self.centralize()
    Solid.__init__(self, self.instance)
  