from .core import _AbstractObject


class Function (_AbstractObject):
    """Represents any function. Parent class for the classes below"""
    
    _i_function = None
    def __init__(self, function):
        assert hasattr(function, "__call__"), "must supply a function"
        self._i_function = function


class AggregationFunction (Function):
    """Represents an aggregation function taking any number of values and
    returning an "aggregate" of some kind, such as the min, max, mean, or
    sum."""
    
    def __call__(self, values):
        """values: iterable of numbers"""
        return self._i_function(values)
        
        
class ResponsibilityFunction (Function):
    """Represents a responsibility function taking a tree, a group, and a node
    and returning an assessment of that group's pointwise, backward, or forward
    responsibility at that node.""" 
    
    def __call__(self, tree=None, group=None, node=None):
        return self._i_function(tree=None, group=None, node=None)
        
        
class PointwiseBackwardResponsibilityFunction (ResponsibilityFunction):
    pass


class AggregateBackwardResponsibilityFunction (ResponsibilityFunction):
    pass
    
    
class ForwardResponsibilityFunction (ResponsibilityFunction):
    pass
