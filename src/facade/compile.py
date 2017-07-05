import os
import json
import inspect
import cadmium

module_names = [x for x in os.listdir('.') if x != 'cadmium.py' and x != 'compile.py' and x.endswith('.py')]
module_names = [x.split('.')[0] for x in module_names]

std_classes = [c[0] for c in inspect.getmembers(cadmium, inspect.isclass)]

expressions = {}

for module_name in module_names:
    mod = __import__(module_name)
    classes = [x for x in inspect.getmembers(mod, inspect.isclass) if x[0] not in std_classes]

    assert len(classes) == 1
    usolid = classes[0][1]()
    expressions[module_name] = dict(
        name=classes[0][0],
        csg=usolid.toData()
    )

open('expressions.js', 'w').write(json.dumps(expressions, indent=2))
