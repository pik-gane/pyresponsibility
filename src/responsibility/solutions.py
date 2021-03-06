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
    """A combination of a certain node representing the current state,
    plus a combination of choices assumed to be made by "nature" at PossibilityNodes
    and ProbabilityNodes and choices assumed to be made by all players outside 
    a certain group at certain nodes in the anchor node's branch. Might be 
    complete or incomplete.""" 
    
    _i_current_node = None
    @property
    def current_node(self):
        """Node"""
        return self._i_current_node

    cu = current_node
    
    def validate(self):
        assert isinstance(self.current_node, nodes.Node), "current_node must be a Node"
        assert isinstance(self.transitions, dict)
        for source, target in self.transitions.items():
            assert ((isinstance(source, nodes.InnerNode) and target in source.successors) 
                    or (isinstance(source, nodes.InformationSet) and target in source.actions))
                    
    def sub_scenario(self, action):
        """Return the subscenario in which action was taken in current_node"""
        return Scenario(self.name + "_" + action.name, 
                        current_node=self.current_node.consequences[action],
                        transitions=self.transitions)
                        
    sub = sub_scenario
    """Abbreviation for sub_scenario"""
    
Scen = Scenario
"""Abbreviation for Scenario"""

    
class Strategy (_AbstractObject):
    """Represents a combination of choices made by the players in a certain group. 
    Might be complete or incomplete.""" 
    
    _i_choices = None
    @property
    def choices(self): 
        """dict of InformationSet: Action"""
        return self._i_choices
    
    def validate(self):
        assert isinstance(self.choices, dict), "choices must be a dict" 
        for ins, ac in self.choices.items():
            assert isinstance(ins, nodes.InformationSet), "choices maps InformationSets to actions"
            assert ac in ins.actions, "choices maps information sets to feasible actions"    

    def includes(self, choices):
        """Return whether the given choices are part of this strategy"""
        return set(choices.items()).issubset(set(self.choices.items()))
        
Strat = Strategy
"""Abbreviation for Strategy"""
