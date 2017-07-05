'''
Python library for Solid Modelling
'''
from __future__ import absolute_import

from builtins import str
import os

from OCC.gp import (gp_Ax1, gp_Pnt, gp_Dir)

from . import solid
from .primitives import cylinder
from .primitives import sphere
from .primitives import box
from .primitives import cone
from .primitives import wedge
from .primitives import torus
from .primitives import text
from .primitives import revolution
from .primitives import extrusion

X_axis = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0))
Y_axis = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 0))
Z_axis = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))

Cylinder = primitives.cylinder.Cylinder
Sphere = primitives.sphere.Sphere
Box = primitives.box.Box
Cone = primitives.cone.Cone
Wedge = primitives.wedge.Wedge
Torus = primitives.torus.Torus
Glyph = primitives.text.Glyph
Text = primitives.text.Text
Revolution = primitives.revolution.Revolution
Extrusion = primitives.extrusion.Extrusion

Solid = solid.Solid

inspectionData = {
    'solidData': {},
    'paramData': {}
}

# Value range constants
POSITIVE = 1
NEGATIVE = 2

# Alignment constants
A_MIN = 1
A_MAX = 2
A_CENTER = 3

# Custom data type
enum = 1

try:
    _brep_cache_path_ = os.path.join(os.environ['HOME'], '.cadmium', 'brepcache')
except KeyError:
    _brep_cache_path_ = os.path.join(os.environ['USERPROFILE'], '.cadmium', 'brepcache')
_brep_caching_enabled_ = True
try:
    _font_dir_ = os.path.join(os.environ['HOME'], '.cadmium', 'fonts')
except KeyError:
    _font_dir_ = os.path.join(os.environ['USERPROFILE'], '.cadmium', 'fonts')
_abs_fontpath_allowed_ = True

if not os.path.exists(_brep_cache_path_):
    os.makedirs(_brep_cache_path_)


#
# Annotation decorators
#
def description(*arg, **kwdArg):
    validArgs = ['shortName', 'summary', 'alignment']
    for k in list(kwdArg.keys()):
        if not (k in validArgs):
            raise Exception('Invalid argument ' + str(k))

    if arg:
        raise Exception('Only named arguments supported')

    import cadmium
    cadmium.inspectionData['solidData'] = kwdArg

    def decorator(func):
        return func

    return decorator


def param(*arg, **kwdArg):
    validArgs = ['name', 'shortName', 'description',
                 'valueRange', 'valueType', 'invalidValues', 'validValues', 'endpointInclusion']
    for k in list(kwdArg.keys()):
        if not (k in validArgs):
            raise Exception('Invalid argument ' + str(k))

    if arg:
        raise Exception('Only named arguments supported')

    import cadmium
    if 'valueType' in kwdArg:
        if kwdArg['valueType'] == int:
            kwdArg['valueType'] = 'int'
        elif kwdArg['valueType'] == float:
            kwdArg['valueType'] = 'float'
        elif kwdArg['valueType'] == str:
            kwdArg['valueType'] = 'str'
        elif kwdArg['valueType'] == bool:
            kwdArg['valueType'] = 'bool'
        elif kwdArg['valueType'] == cadmium.enum:
            kwdArg['valueType'] = 'enum'
        else:
            kwdArg['valueType'] = 'unknown'

    cadmium.inspectionData['paramData'][kwdArg['name']] = kwdArg

    def decorator(func):
        return func

    return decorator


class CadmiumException(BaseException):
    '''
    Useful mainly for validating user provided input for Solid instantiations
    '''

    def __init__(self, msg):
        self.msg = msg
        BaseException.__init__(self, msg)


def garbage_collect():
    GarbageCollector.garbage.smart_purge()
