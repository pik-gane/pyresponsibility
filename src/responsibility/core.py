import itertools 
import numpy as np
import sympy as sp

# _c_...: class attr must be set at class def
# _i_...: must be set at init
# _a_...: will be computed automatically and validated lazily and cached
    
abbreviations = {
    "ac": "is_acceptable",
    "ch": "choices",
    "co": "consequences",
    "pl": "player",
    "pr": "probabilities",
    "su": "successors",
    "ou": "outcome",
    "tr": "transitions",
    }
        
class _AbstractObject (object):

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
        assert len(name) > 0
        self._i_name = name
        for attr, value in kwargs.items():
            if attr in abbreviations: attr = abbreviations[attr]
            assert hasattr(self, "_i_"+attr)
            setattr(self, "_i_"+attr, value)
        self.validate()
        
    def validate(self): pass

    def __str__(self): return self._i_name
    def __repr__(self): return self._i_name

    


    



    

        

class Function (_AbstractObject):
    _i_function = None
    def __init__(self, function):
        assert hasattr(function, "__call__"), "must supply a function"
        self._i_function = function

class AggregationFunction (Function):
    def __call__(self, values):
        """values: iterable of numbers"""
        return self._i_function(values)
        
class ResponsibilityFunction (_AbstractObject):
    def __call__(self, tree=None, group=None, node=None):
        return self._i_function(tree=None, group=None, node=None)
        
class PointwiseBackwardResponsibilityFunction (ResponsibilityFunction):
    pass

class AggregateBackwardResponsibilityFunction (ResponsibilityFunction):
    pass
    
class ForwardResponsibilityFunction (ResponsibilityFunction):
    pass

