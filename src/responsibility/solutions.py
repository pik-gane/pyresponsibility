from .core import _AbstractObject
from . import nodes


class PartialSolution (_AbstractObject):
    """Represents a set of transitions between nodes.
    Parent class of Scenario"""
    
    _i_transitions = None
    @property
    def transitions(self):
        """dict of InnerNode: successor Node"""
        return self._i_transitions
        
    def validate(self):
        assert isinstance(self.transitions, dict)
        for source, target in self.transitions.items():
            assert ((isinstance(source, nodes.InnerNode) and target in source.successors) 
                    or (isinstance(source, nodes.InformationSet) and target in source.actions))

            
class Scenario (PartialSolution):
    """Represents a combination of choices made by "nature" at PossibilityNodes
    and ProbabilityNodes and choices made by all players outside a certain group""" 
    
    _i_anchor = None
    @property
    def anchor(self):
        """Node"""
        return self._i_anchor

    def validate(self):
        assert isinstance(self.anchor, nodes.Node), "anchor must be a Node"
        assert isinstance(self.transitions, dict)
        for source, target in self.transitions.items():
            assert ((isinstance(source, nodes.InnerNode) and target in source.successors) 
                    or (isinstance(source, nodes.InformationSet) and target in source.actions))

    
class Strategy (_AbstractObject):
    """Represents a combination of choices made by the players in a certain group""" 
    
    _i_anchor = None
    @property
    def anchor(self):
        """Node"""
        return self._i_anchor

    _i_choices = None
    @property
    def choices(self): 
        """dict of InformationSet: Action"""
        return self._i_choices
    
    def validate(self):
        assert isinstance(self.anchor, nodes.Node), "anchor must be a Node"
        assert isinstance(self.choices, dict), "choices must be a dict" 
        for ins, ac in self.choices.items():
            assert isinstance(ins, nodes.InformationSet), "choices maps InformationSets to actions"
            assert ac in ins.actions, "choices maps information sets to feasible actions"    

