import random
import sympy as sp

from .core import _AbstractObject, hasname

from .actions import Action
from .outcomes import Outcome
from .players import Player
from . import trees


class Node (_AbstractObject):

    _c_dotshape = "oval"

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
            self._a_branch = trees.Branch("_br_" + self.name, root=self)
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

    def __repr__(self):
        return self.name if hasname(self) else "•"

    def _to_lines(self, pre1, pre2):
        return "\n" + pre1 + repr(self)
        
    _a_dotname = None
    def _get_dotname(self):
        if self._a_dotname is None:
            self._a_dotname = self.name if hasname(self) else "_" + str(random.random())
        return self._a_dotname

    def _add_to_dot(self, dot):
        dot.node(self._get_dotname(), 
                 (self.name if hasname(self) else "")
                 + ("\n" if hasname(self) and hasattr(self, "player") else "")
                 + (self.player.name if hasattr(self, "player") else ""),
                 shape=self._c_dotshape)
        
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

    def __repr__(self):
        return Node.__repr__(self) + " …"
        
    def _to_lines(self, pre1, pre2):
        su = list(self.successors)
        return ("\n" + pre1 + Node.__repr__(self)
                + "".join([v._to_lines(pre2 + "├─╴", pre2 + "│  ") for v in su[:-1]])
                + su[-1]._to_lines(pre2 + "╰─╴", pre2 + "   "))

    def _add_to_dot(self, dot):
        Node._add_to_dot(self, dot)
        for v in self.successors:
            v._add_to_dot(dot)
            dot.edge(self._get_dotname(), v._get_dotname())

class LeafNode (Node):
    pass

    
class PossibilityNode (InnerNode):
    """A node representing an uncertainty whose potential realizations have
    no known probabilities. This is often metaphorically called a decision
    to be taken by "nature".
    
    @param successors: A set of Nodes or (label, Node) pairs representing the
    possible successor nodes.
    @param labels: An optional dict of labels keyed by successor Node. These
    labels will be placed on the arrows connecting this node to its successors. 
    """

    _c_dotshape = "diamond"

    _i_labels = None
    @property
    def labels(self):
        """dict of labels keyed by successor Node"""
        return self._i_labels

    def validate(self):
        if self.labels is None:
            self._i_labels = {}
        assert isinstance(self.successors, set)
        for node in list(self.successors):
            if isinstance(node, tuple):
                self.successors.remove(node)
                label, node = node
                self.successors.add(node)
                self.labels[node] = label
            assert isinstance(node, Node)
        assert isinstance(self.labels, dict)
        for v, l in self.labels.items():
            assert v in self.successors
            assert isinstance(l, str)

    def _to_lines(self, pre1, pre2):
        su = list(self.successors)
        la = self.labels
        return ("\n" + pre1 + Node.__repr__(self)
                + "".join([(
                    v._to_lines(pre2 + "├─╴" + la[v] + "╶─╴", pre2 + "│     " + " "*len(la[v])) 
                    if v in la and la[v] != "" 
                    else v._to_lines(pre2 + "├─╴", pre2 + "│  ")
                    ) for v in su[:-1]])
                + (su[-1]._to_lines(pre2 + "╰─╴" + la[su[-1]] + "╶─╴", pre2 + "      " + " "*len(la[su[-1]])) 
                   if su[-1] in la and la[su[-1]] != ""
                   else su[-1]._to_lines(pre2 + "╰─╴", pre2 + "   "))
                )

    def _add_to_dot(self, dot):
        Node._add_to_dot(self, dot)
        for v in self.successors:
            v._add_to_dot(dot)
            dot.edge(self._get_dotname(), v._get_dotname(),
                     label=self.labels.get(v, ""))

PoN = PossibilityNode

    
class ProbabilityNode (InnerNode):
    
    _c_dotshape = "rect"

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

    def __repr__(self):
        return Node.__repr__(self) + " ⚄ …"

    def _to_lines(self, pre1, pre2):
        su = list(self.probabilities.items())
        return ("\n" + pre1 + Node.__repr__(self)
                + "".join([v._to_lines(pre2 + "├─╴" + str(p) + "╶─╴", pre2 + "│     " + " "*len(str(p)) ) for v, p in su[:-1]])
                + su[-1][0]._to_lines(pre2 + "╰─╴" + str(su[-1][1]) + "╶─╴", pre2 + "      " + " "*len(str(su[-1][1]))))
            
    def _add_to_dot(self, dot):
        Node._add_to_dot(self, dot)
        for v, p in self.probabilities.items():
            v._add_to_dot(dot)
            dot.edge(self._get_dotname(), v._get_dotname(), label=str(p))

PrN = ProbabilityNode

class DecisionNode (InnerNode):

    _c_dotshape = "diamond"

    _i_player = None
    @property
    def player(self): 
        return self._i_player
    
    _i_consequences = None
    @property
    def consequences(self):
        """dict of Action: successor Node"""
        return self._i_consequences
        
    _i_information_set = None
    @property
    def information_set(self):
        if self._i_information_set is None:
            InformationSet("_ins_" + self.name, nodes={self})
        return self._i_information_set

    def validate(self):
        assert isinstance(self.player, Player)
        assert isinstance(self.consequences, dict)
        actions = self._a_actions = set(self.consequences.keys())
        self._i_successors = set(self.consequences.values())
        assert len(actions) > 0, "decision node must have at least one action"
        for action, node in self.consequences.items():
            assert isinstance(action, Action)
            assert isinstance(node, Node)
        if self._i_information_set is not None:
            self._i_information_set.add_node(self)
    
    _a_actions = None
    @property
    def actions(self): 
        """Set of possible Actions"""
        if self._a_actions is None:
            self.validate()
        return self._a_actions

    def _base_repr(self):
        return (Node.__repr__(self) 
                + (" (" + self.information_set.name + ")" if len(self.information_set.nodes) > 1 else "")
                + ": " + repr(self.player))
        
    def __repr__(self):
        return self._base_repr() + " …"
 
    def _to_lines(self, pre1, pre2):
        su = list(self.consequences.items())
        return ("\n" + pre1 + self._base_repr()
                + "".join([v._to_lines(pre2 + "├─╴" + repr(a) + "╶─╴", pre2 + "│     " + " "*len(repr(a))) for a, v in su[:-1]])
                + su[-1][1]._to_lines(pre2 + "╰─╴" + repr(su[-1][0]) + "╶─╴", pre2 + "      " + " "*len(repr(su[-1][0]))))

    def _add_to_dot(self, dot):
        Node._add_to_dot(self, dot)
        for a, v in self.consequences.items():
            v._add_to_dot(dot)
            dot.edge(self._get_dotname(), v._get_dotname(), label=a.name)
        vs = list(self.information_set.nodes)
        if len(vs) > 1 and vs[0] == self:
            with dot.subgraph(edge_attr={"dir": "none", 
                                         "constraint": "false", 
                                         "style": "dashed"}) as sub:
                v1 = self
                for v2 in vs[1:]:
                    sub.edge(v1._get_dotname(), v2._get_dotname(),
                             headlabel=" " + self.information_set.name + " " if v1==self else "",
                             len="0.0001")
                    v1 = v2


DeN = DecisionNode


class OutcomeNode (LeafNode):

    _c_symbols = ["vo"]

    _i_outcome = None
    @property
    def outcome(self): 
        return self._i_outcome

    def validate(self):
        assert isinstance(self.outcome, Outcome)

    def __repr__(self):
        return Node.__repr__(self) + ": " + repr(self.outcome)

    def _to_lines(self, pre1, pre2):
        return "\n" + pre1 + repr(self)

    def _add_to_dot(self, dot):
        Node._add_to_dot(self, dot)
        o = self.outcome
        dot.node(o.name, shape="triangle" if o.is_acceptable else "invtriangle")
        dot.edge(self._get_dotname(), o.name, dir="none", len="1000.0")

        
OuN = OutcomeNode


class InformationSet (_AbstractObject):
    
    _i_nodes = None
    @property
    def nodes(self):
        """Set of DecisionNodes, each having its information_set=this"""
        return self._i_nodes

    def __init__(self, name, **kwargs):
        self._i_nodes = set()
        super(InformationSet, self).__init__(name, **kwargs)
        for node in self.nodes:
            assert node._i_information_set is None, "node can only be in one information set"
            node._i_information_set = self

    def add_node(self, node):
        self._i_nodes.add(node)
        self.validate()
        
    def validate(self):
        assert isinstance(self.nodes, set), "information set must be a set of DecisionNodes"
        if len(self.nodes) > 0:
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
        
    def __repr__(self):
        return (self.name + ": " if hasname(self) else "") + repr(self.nodes)

InS = InformationSet
