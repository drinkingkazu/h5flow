from inspect import isclass
import os
import importlib.util
import sys
from pkgutil import iter_modules

def find_class(classname, directory):
    path = directory
    for (finder, name, _) in iter_modules([path]):
        if name == 'setup' or name == 'h5flow':
            continue
        spec = finder.find_spec(name)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if isclass(attribute):
                if attribute_name == classname:
                    return attribute
    return None

def get_class(classname):
    # first search in local directory
    found_class = find_class(classname, './')

    if found_class is None:
        # search for h5flow_modules directory
        found_class = find_class(classname, './h5flow_modules/')

        # then recurse into h5flow_modules subdirectories
        if found_class is None:
            for parent, dirs, files in os.walk('./h5flow_modules/'):
                for directory in dirs:
                    found_class = find_class(classname, os.path.join(parent,directory))
                    if found_class is not None:
                        break
                if found_class is not None:
                        break

        if found_class is None:
            # then search in source
            found_class = find_class(classname, os.path.dirname(__file__))

    if found_class is None:
        raise RuntimeError(f'no matching class {classname} found!')

    return found_class
