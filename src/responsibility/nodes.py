import sympy as sp

from .core import _AbstractObject

from .actions import Action
from .outcomes import Outcome
from .players import Player
from . import trees


class Node (_AbstractObject):

    _c_symbols = ["v"]

    _a_predecessor = None
    @property
    def predecessor(self):
        """predecessor Node if not is_root"""
        return self._a_predecessor

    _a_branch = None
    @property
    def branch(self):
        """the Branch starting at this node"""
        if self._a_branch is None:
            self._a_branch = trees.Branch(self)
        return self._a_branch

    _a_history = None
    @property
    def history(self):
        """list of Nodes from root to predecessor"""
        if self._a_history is None:
            if self.predecessor is None:
                self._a_history = []
            else:
                self._a_history = self.predecessor.history + [self.predecessor]
        return self._a_history

    _a_tree = None
    @property
    def tree(self):
        """the whole Tree containing this node"""
        if self._a_tree is None:
            self._a_tree = trees.Tree((self.history + [self])[0])
        return self._a_tree


class InnerNode (Node):

    _i_successors = None
    @property
    def successors(self):
        """Set of successor Nodes"""
        return self._i_successors

    def __init__(self, name, **kwargs):
        super(InnerNode, self).__init__(name, **kwargs)
        for node in self._i_successors:
            assert node._a_predecessor is None, "node can only have one predecessor"
            node._a_predecessor = self

class LeafNode (Node):
    pass

    
class PossibilityNode (InnerNode):
#    _c_symbols = ["?"]

    def validate(self):
        assert isinstance(self.successors, set)
        for node in self.successors:
            assert isinstance(node, Node)

PoN = PossibilityNode

    
class ProbabilityNode (InnerNode):
    _c_symbols = ["vp"]
    
    _i_probabilities = None
    @property
    def probabilities(self):
        """dict of successor Node: probability 0...1"""
        return self._i_probabilities

    def validate(self):
        assert isinstance(self.probabilities, dict)
        self._i_successors = set(self.probabilities.keys())
        total_p = 0
        for node, p in self.probabilities.items():
            assert isinstance(node, Node)
            total_p += p
        if isinstance(total_p, sp.Expr):
            total_p = sp.simplify(total_p)
        assert total_p == 1, "sum of probability values must be 1" 

PrN = ProbabilityNode


class DecisionNode (InnerNode):

    _c_symbols = ["vd"]

    _i_player = None
    @property
    def player(self): 
        return self._i_player
    
    _i_consequences = None
    @property
    def consequences(self):
        """dict of Action: successor Node"""
        return self._i_consequences
        
    def validate(self):
        assert isinstance(self.player, Player)
        assert isinstance(self.consequences, dict)
        actions = self._a_actions = set(self.consequences.keys())
        self._i_successors = set(self.consequences.values())
        assert len(actions) > 0, "decision node must have at least one action"
        for action, node in self.consequences.items():
            assert isinstance(action, Action)
            assert isinstance(node, Node)
    
    _a_actions = None
    @property
    def actions(self): 
        """Set of possible Actions"""
        if self._a_actions is None:
            self.validate()
        return self._a_actions

    _a_information_set = None
    @property
    def information_set(self):
        if self._a_information_set is None:
            InformationSet("_ins_" + self.name, nodes={self})
        return self._a_information_set

DeN = DecisionNode


class OutcomeNode (LeafNode):

    _c_symbols = ["vo"]

    _i_outcome = None
    @property
    def outcome(self): 
        return self._i_outcome

    def validate(self):
        assert isinstance(self.outcome, Outcome)

OuN = OutcomeNode


class InformationSet (_AbstractObject):
    
    _i_nodes = None
    @property
    def nodes(self):
        """Set of DecisionNodes, each having its information_set=this"""
        return self._i_nodes

    def __init__(self, name, **kwargs):
        super(InformationSet, self).__init__(name, **kwargs)
        for node in self._i_nodes:
            assert node._a_information_set is None, "node can only be in one information set"
            node._a_information_set = self
        
    def validate(self):
        assert isinstance(self.nodes, set), "information set must be a set of DecisionNodes"
        assert len(self.nodes) > 0, "information set cannot be empty"
        self._a_player = list(self.nodes)[0].player
        for node in self.nodes:
            assert isinstance(node, DecisionNode), "nodes in information set must be DecisionNodes"
            assert node.player == self._a_player, "all nodes in information set must belong to the same player"

    _a_player = None
    @property
    def player(self):
        if self._a_player is None:
            self.validate()
        return self._a_player 
               
    _a_actions = None
    @property
    def actions(self): 
        """Set of possible Actions"""
        if self._a_actions is None:
            for node in self._i_nodes:
                actions = set(node.consequences.keys())
                if self._a_actions is None:
                    self._a_actions = actions
                else:
                    assert self._a_actions == actions
        return self._a_actions

    def __contains__(self, node):
        return node in self._i_nodes

InS = InformationSet
