from .core import _AbstractObject


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
