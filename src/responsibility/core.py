import sys
import types
import itertools 
import numpy as np
import sympy as sp
from line_profiler import LineProfiler
profile = LineProfiler()

# _c_...: class attr must be set at class def
# _i_...: must be set at init
# _a_...: will be computed automatically and validated lazily and cached
    
abbreviations = {
    "ac": "is_acceptable",
    "ch": "choices",
    "co": "consequences",
    "ins": "information_set",
    "la": "labels",
    "no": "nodes",
    "pl": "player",
    "pr": "probabilities",
    "ro": "root",
    "su": "successors",
    "ou": "outcome",
    "tr": "transitions",
    }
        
class _AbstractObject (object):
    """Parent class for objects that have a name and optionally a description,
    such as Agent, Group, Action, Outcome, Node."""

    _c_symbols = []
    @property
    @classmethod
    def symbols(cls):
        """list of symbols for generic objects of this type"""
        return cls._c_symbols
        
    _i_name = ""
    @property
    def name(self):
        """short and unique name of object"""
        return self._i_name
        
    _i_desc = ""
    @property
    def desc(self):
        """optional longer description"""
        return self._i_desc
    
    def __init__(self, name, **kwargs):
        assert isinstance(name, str)
        self._i_name = name
        for attr, value in kwargs.items():
            if attr in abbreviations: attr = abbreviations[attr]
            assert hasattr(self, "_i_"+attr)
            if isinstance(value, set):
                value = frozenset(value)
            setattr(self, "_i_"+attr, value)
        self.validate()
        
    def validate(self): pass

    def __str__(self): return self._i_name
    
    def __repr__(self): return self._i_name


# helper functions:
    
def hasname(ob):
    """Does the object have a name that begins with a letter?""" 
    return hasattr(ob, "name") and isinstance(ob.name, str) and len(ob.name)>0 and ob.name[0].isalpha()
    
def update_consistently(base, other):
    """Update base dict with other dict until a conflict is found.
    Returns whether a conflict was found.""" 
    for key, value in other.items():
        if base.setdefault(key, value) != value:
            # attempted update is inconsistent with content, so stop here
            return False
    return True    
    
def global_symbols(*names):
    """Create a sympy symbol for each name listed as an argument 
    and store it in a global variable of the same name"""
    module_name = list(sys._current_frames().values())[0].f_back.f_globals['__name__']
    module = sys.modules[module_name]
    sy = sp.symbols(",".join([*names]))
    for s in sy if isinstance(sy, tuple) else [sy]:
        n = s.name
        if getattr(module, n, s) != s:
            print("Warning: global var", n, "existed, did not overwrite it.")
        else:
            setattr(module, n, s)

def Min(*args):
    if isinstance(args[0], (list, types.GeneratorType)):
        assert len(args)==1
        values = [*args[0]]
    else:
        values = [*args]
    return (sp.simplify(sp.Min(*values)) if np.any([isinstance(v, sp.Expr) for v in values])
            else min(*values))

def Max(*args):
    if isinstance(args[0], (list, types.GeneratorType)):
        assert len(args)==1
        values = [*args[0]]
    else:
        values = [*args]
    return (sp.simplify(sp.Max(*values)) if np.any([isinstance(v, sp.Expr) for v in values])
            else max(*values))
