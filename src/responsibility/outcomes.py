import sys
import numpy as np

from .core import _AbstractObject, hasname


class Outcome (_AbstractObject):
    """Represents an outcome attached to one or more outcome nodes,
    and states whether it is ethically acceptable"""

    _i_is_acceptable = None
    @property
    def is_acceptable(self):
        """bool"""
        return self._i_is_acceptable

    def __init__(self, name, **kwargs):
        self._a_nodes = []
        super(Outcome, self).__init__(name, **kwargs)

    _a_nodes = None
    @property
    def nodes(self):
        """Set of DecisionNodes, each having its information_set=this"""
        return self._a_nodes

    def add_node(self, node):
        if node not in self.nodes:
            self._a_nodes.append(node)
        self.validate()
        
    def validate(self):
        assert isinstance(self.is_acceptable, (bool, np.bool_))

    def __repr__(self):
        return (self.name + " " if hasname(self) else "") + ("✔" if self.is_acceptable else "✖")

Ou = Outcome
"""Abbreviation for Outcome"""

def outcomes(*names, is_acceptable=None):
    """Return an Outcome for each name listed as an argument"""
    return tuple(Outcome(name, is_acceptable=is_acceptable) for name in names)
    
def global_outcomes(*names, is_acceptable=None):
    """Create a Outcome for each name listed as an argument 
    and store it in a global variable of the same name"""
    module_name = list(sys._current_frames().values())[0].f_back.f_globals['__name__']
    module = sys.modules[module_name]
    for ou in outcomes(*names, is_acceptable=is_acceptable):
        n = ou.name
        if getattr(module, n, ou) != ou:
            print("Warning: global var", n, "existed, did not overwrite it.")
        else:
            setattr(module, n, ou)
