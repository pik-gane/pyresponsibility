import sys

from .core import _AbstractObject


class Action (_AbstractObject):

    _c_symbols = ["a", "b"]

Ac = Action

def actions(*names):
    """Return an Action for each name listed as an argument"""
    return (Action(name) for name in names)
    
def global_actions(*names):
    """Create an Action for each name listed as an argument 
    and store it in a global variable of the same name"""
    module_name = list(sys._current_frames().values())[0].f_back.f_globals['__name__']
    module = sys.modules[module_name]
    for a in actions(*names):
        n = a.name
        if getattr(module, n, a) != a:
            print("Warning: global var", n, "existed, did not overwrite it.")
        else:
            setattr(module, n, a)
