from .core import _AbstractObject
from .nodes import *
from .players import *
from .trees import *


class Function (_AbstractObject):
    """Represents any function. Parent class for the classes below"""
    
    _i_function = None
    def __init__(self, name, function=None, **kwargs):
        assert hasattr(function, "__call__"), "must supply a function"
        self._i_function = function
        super(Function, self).__init__(name, **kwargs)

Fct = Function
"""Abbreviation for Function"""


class AggregationFunction (Function):
    """Represents an aggregation function taking any number of values and
    returning an "aggregate" of some kind, such as the min, max, mean, or
    sum."""
    
    def __call__(self, values):
        """values: iterable of numbers"""
        return self._i_function(values)
        
AggF = AggregationFunction
"""Abbreviation for AggregationFunction"""

        
class ResponsibilityFunction (Function):
    """Represents a responsibility function taking a tree, a group, and a node
    and returning an assessment of that group's backward, or forward
    responsibility at that node.""" 
    
    def __call__(self, tree=None, group=None, node=None):
        assert isinstance(tree, Tree)
        assert isinstance(group, Group)
        assert isinstance(node, Node)
        assert node.path[0] == tree.root
        return self._i_function(tree, group, node)

RespF = ResponsibilityFunction
"""Abbreviation for ResponsibilityFunction"""


class PointwiseResponsibilityFunction (Function):
    """Represents a "pointwise" responsibility function taking a tree, a group, 
    a decision node, and an action, and returning an assessment of that group's
    responsibility due to having taken that action at that node.""" 
    def __call__(self, tree=None, group=None, node=None, action=None):
        assert isinstance(tree, Tree)
        assert isinstance(group, Group)
        assert isinstance(node, DecisionNode)
        assert node.path[0] == tree.root
        assert node.player in group
        assert action in node.actions
        return self._i_function(tree, group, node, action)

PRF = PointwiseResponsibilityFunction
"""Abbreviation for PointwiseResponsibilityFunction"""


class BackwardResponsibilityFunction (ResponsibilityFunction):
    """Represents a backward responsibility function taking a tree, a group, 
    and an outcome node, and returning an assessment of that group's 
    (factual or counterfactual) backward responsibility for an unacceptable 
    outcome due to having taken the actions they took on the way to this
    outcome node.""" 
    def __call__(self, tree=None, group=None, node=None):
        assert isinstance(tree, Tree)
        assert isinstance(group, Group)
        assert isinstance(node, OutcomeNode)
        assert node.path[0] == tree.root
        return self._i_function(tree, group, node)
    
BRF = BackwardResponsibilityFunction
"""Abbreviation for BackwardResponsibilityFunction"""


class ForwardResponsibilityFunction (ResponsibilityFunction):
    """Represents a forward responsibility function taking a tree, a group, 
    and a decision node, and returning an assessment of that group's forward
    responsibility for avoiding an unacceptable outcome when in this node.""" 
    def __call__(self, tree=None, group=None, node=None):
        assert isinstance(tree, Tree)
        assert isinstance(group, Group)
        assert isinstance(node, DecisionNode)
        assert node.path[0] == tree.root
        assert node.player in group
        return self._i_function(tree, group, node)
    
FRF = ForwardResponsibilityFunction
"""Abbreviation for ForwardResponsibilityFunction"""


