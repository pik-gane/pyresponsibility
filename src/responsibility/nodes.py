import sys
import random
import sympy as sp

from .core import _AbstractObject, hasname

from .actions import Action
from .outcomes import Outcome
from .players import Player
from . import trees


class Node (_AbstractObject):
    """Parent class for all types of nodes"""

    _c_dotshape = "oval"
    """Shape used in rendering via graphviz"""

    def remove(self):
        """called when removed from the tree, performs cleanup"""
        pass

    _a_predecessor = None
    @property
    def predecessor(self):
        """Predecessor Node if not is_root"""
        return self._a_predecessor

    pred = predecessor
    
    @property
    def path(self):
        """List of Nodes from root to self"""
        return [self] if self.predecessor is None else self.predecessor.path + [self]
        # Note: cannot be cached since it is mutable!
        
    _a_branch = None
    @property
    def branch(self):
        """The Branch starting at this node"""
        if self._a_branch is None:
            self._a_branch = trees.Branch("_br_" + self.name, root=self, total_recall=False)
        return self._a_branch

    _a_tree = None
    @property
    def tree(self):
        """The whole (!) Tree containing this node 
        (not just the branch starting here)"""
        if self._a_tree is None:
            self._a_tree = trees.Tree("T_" + self.name, ro=self.path[0])
        return self._a_tree

    def __repr__(self):
        """Short string representation"""
        return self.name if hasname(self) else "•"

    def _to_lines(self, pre1, pre2):
        """Generate one or more lines for the detailed description of a branch"""
        return "\n" + pre1 + repr(self)
        
    _a_dotname = None
    def _get_dotname(self):
        """Get an id to be used internally in the graphviz file"""
        if self._a_dotname is None:
            self._a_dotname = self.name if hasname(self) else "_" + str(random.random())
        return self._a_dotname

    def _add_to_dot(self, dot):
        """Add this node to the graphviz ("dot") file"""
        dot.node(self._get_dotname(), 
                 (self.name if hasname(self) else "")
                 + ("\n" if hasname(self) and hasattr(self, "player") else "")
                 + (self.player.name if hasattr(self, "player") else ""),
                 shape=self._c_dotshape,
                 penwidth="3.0" if getattr(self, 'highlight', False) else "1.0"
                 )
        
        
class InnerNode (Node):
    """Parent class for all nodes whith have at least one successor node"""

    _i_successors = None
    @property
    def successors(self):
        """Set of successor Nodes"""
        return self._i_successors

    su = successors

    def __init__(self, name, **kwargs):
        super(InnerNode, self).__init__(name, **kwargs)
        for node in self._i_successors:
            assert node._a_predecessor is None, "node can only have one predecessor"
            node._a_predecessor = self

    def remove(self):
        """called when removed from the tree, performs cleanup"""
        for v in self.successors:
            v.remove()
        super(InnerNode, self).remove()

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
    """Parent class for all leaf nodes (currently only OutcomeNode)"""
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
        assert isinstance(self.successors, frozenset)
        su = []
        for node in self.successors:
            if isinstance(node, tuple):
                label, node = node
                self.labels[node] = label
            assert isinstance(node, Node)
            su.append(node)
        self._i_successors = frozenset(su)
        assert isinstance(self.labels, dict)
        for v, l in self.labels.items():
            assert v in self.successors
            assert isinstance(l, str)

    def clone(self, subs=None, keep=None):
        """Return a deep copy of this Node and all its descendants as an 
        independent clone with no connections to this node's branch. Use
        subs to replace information sets and outcomes"""
        if subs is None:
            subs = {}
        subs[self] = clone = PossibilityNode(self.name, desc=self.desc, su={
            v.clone(subs=subs, keep=keep) 
            if self.labels is None
            else (self.labels.get(v, ""), v.clone(subs=subs, keep=keep))
            for v in self.successors
            if keep is None or v in keep
        })
        return clone

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
"""Abbreviation for PossibilityNode"""

    
class ProbabilityNode (InnerNode):
    """A node representing a stochastic event with known probabilities.
    @param probabilities: dict of probabilities keyed by successor Node.
    Values can be numbers or sympy expressions.
    """
    
    _c_dotshape = "rect"

    _i_probabilities = None
    @property
    def probabilities(self):
        """Dict of successor Node: probability 0...1"""
        return self._i_probabilities

    pr = probabilities
    
    _i_labels = None
    @property
    def labels(self):
        """dict of labels keyed by successor Node"""
        return self._i_labels

    def validate(self):
        if self.labels is None:
            self._i_labels = {}
        assert isinstance(self.probabilities, dict)
        # if necessary, extract labels from probabalities dict:
        pr = {}
        for node, p in self.probabilities.items():
            if isinstance(node, tuple):
                label, node = node
                self.labels[node] = label
            assert isinstance(node, Node)
            pr[node] = p
        self._i_probabilities = pr
        self._i_successors = set(self.probabilities.keys())
        total_p = 0
        for node, p in self.probabilities.items():
            assert isinstance(node, Node)
            total_p += p
        if isinstance(total_p, sp.Expr):
            total_p = sp.simplify(total_p)
        assert total_p == 1, "sum of probability values must be 1" 
        assert isinstance(self.labels, dict)
        for v, l in self.labels.items():
            assert v in self.successors
            assert isinstance(l, str)

    def clone(self, subs=None, keep=None):
        """Return a deep copy of this Node and all its descendants as an 
        independent clone with no connections to this node's branch. Use
        subs to replace information sets and outcomes"""
        if subs is None:
            subs = {}
        ptotal = 0
        for v, p in self.probabilities.items():
            if (keep is None or v in keep):
                ptotal += p
                if isinstance(p, sp.Expr):
                    for s in p.free_symbols: 
                        if s not in subs:
                            # reuse expression since sympy does not know about cloning:
                            subs[s] = s
        pr = {
            v.clone(subs=subs, keep=keep): sp.simplify((p/ptotal).subs(subs)) if isinstance(p, sp.Expr) else (p/ptotal)
            for v, p in self.probabilities.items()
            if keep is None or v in keep
        }
        labels = {v: "posterior" for v, p in pr.items()} if ptotal != 1 else None
        subs[self] = clone = ProbabilityNode(self.name, desc=self.desc, pr=pr, labels=labels)
        return clone

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
            dot.edge(self._get_dotname(), v._get_dotname(), 
                     label=(self.labels[v]+": " if v in self.labels else "") + str(p))

PrN = ProbabilityNode
"""Abbreviation for ProbabilityNode"""


class DecisionNode (InnerNode):
    """A node representing a choice of exactly one of several possible named_actions
    to made by some player.
    @param player: the acting Player
    @param consequences: dict of successor Node keyed by Action
    @param information_set: optional InformationSet this node belongs to.
           (alternatively, the InformationSet can also be specified later by
           instantiating an instance of InformationSet and giving it a set of
           DecisionNodes)
    """

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
    
    co = consequences
        
    _i_information_set = None
    @property
    def information_set(self):
        if self._i_information_set is None:
            InformationSet("S_" + self.name, nodes={self})
        return self._i_information_set

    ins = information_set
    """Abbreviation for information_set"""
    
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
            ins = self._i_information_set
            self._i_information_set = None
            ins.add_node(self)
    
    def clone(self, subs=None, keep=None):
        """Return a deep copy of this Node and all its descendants as an 
        independent clone with no connections to this node's branch. Use
        subs to replace information sets and outcomes"""
        if subs is None:
            subs = {}
        if self.ins not in subs:
            # make a fresh information set into which cloned nodes will register:
            subs[self.ins] = InformationSet(self.ins.name, desc=self.ins.desc) 
        if self.player not in subs:
            # clone player:
            subs[self.player] = self.player.clone()
        for a, v in self.consequences.items():
            if keep is None or v in keep:
                if a not in subs:
                    # clone action:
                    subs[a] = a.clone()
        subs[self] = clone = DecisionNode(self.name, desc=self.desc, 
                            pl=subs[self.player], ins=subs[self.ins], co={
            subs[a]: v.clone(subs=subs, keep=keep)
            for a, v in self.consequences.items()
            if keep is None or v in keep
        })
        return clone

    def remove(self):
        """called when removed from the tree, performs cleanup"""
        super(DecisionNode, self).remove()
        self.information_set._i_nodes.remove(self)

    _a_actions = None
    @property
    def actions(self): 
        """Set of possible Actions"""
        if self._a_actions is None:
            self._a_actions = set(self.consequences.keys())
        return self._a_actions

    def get_action(self, successor):
        """Get the action leading to a successor"""
        for a, v in self.consequences.items():
            if v == successor:
                return a
        return None
        
    @property
    def choice_history(self):
        """List of (InformationSet, Action) pairs from root to predecessor"""
        hist = []
        for pos, v in enumerate(self.path[:-1]):
            if isinstance(v, DecisionNode) and v.player == self.player:
                hist.append((v.information_set, v.get_action(self.path[pos+1])))
        return hist
        # Note: cannot be cached since it is mutable!
        
    def _base_repr(self):
        return (Node.__repr__(self) 
                + (" (" + self.information_set.name + ")" if len(self.information_set.nodes) > 1 else "")
                + ": " 
                + repr(self.player))
        
    def __repr__(self):
        return self._base_repr() + " …"
 
    def _to_lines(self, pre1, pre2):
        su = list(self.consequences.items())
        return ("\n" + pre1 + self._base_repr()
                + "".join([v._to_lines(pre2 + "├─╴" + repr(a) + "╶─╴", pre2 + "│     " + " "*len(repr(a))) for a, v in su[:-1]])
                + su[-1][1]._to_lines(pre2 + "╰─╴" + repr(su[-1][0]) + "╶─╴", pre2 + "      " + " "*len(repr(su[-1][0]))))

    def _add_to_dot(self, dot):
        vs = list(self.information_set.nodes)
        if len(vs) > 1:
            if vs[0] == self:
                with dot.subgraph(name="cluster_" + self.information_set.name,
                                  graph_attr={
                                      "label": self.information_set.name,
                                      "style": "dashed",
                                      "penwidth": "3.0" if getattr(self.information_set, 'highlight', False) else "1.0"
                                  }) as sub:
                    for v in vs:
                        Node._add_to_dot(v, sub)
        else:
            Node._add_to_dot(self, dot)
        for a, v in self.consequences.items():
            v._add_to_dot(dot)
            dot.edge(self._get_dotname(), v._get_dotname(), label=a.name)

DeN = DecisionNode
"""Abbreviation for DecisionNode"""


class OutcomeNode (LeafNode):
    """A leaf node representing a situation where no further uncertainty about
    the outcome exists.
    @param outcome: the corresponding Outcome object
    """

    _i_outcome = None
    @property
    def outcome(self): 
        return self._i_outcome

    ou = outcome
    """Abbreviation for outcome"""

    def validate(self):
        assert isinstance(self.outcome, Outcome)
        self.outcome.add_node(self)

    def clone(self, subs=None, keep=None):
        """Return a deep copy of this Node and all its descendants as an 
        independent clone with no connections to this node's branch. Use
        subs to replace information sets and outcomes"""
        if subs is None:
            subs = {}
        if self.ou not in subs:
            # clone outcome:
            subs[self.ou] = self.ou.clone() 
        subs[self] = clone = OutcomeNode(self.name, desc=self.desc, ou=subs[self.ou])
        return clone

    def remove(self):
        """called when removed from the tree, performs cleanup"""
        super(OutcomeNode, self).remove()
        self.outcome._a_nodes.remove(self)

    def __repr__(self):
        return Node.__repr__(self) + ": " + repr(self.outcome)

    def _to_lines(self, pre1, pre2):
        return "\n" + pre1 + repr(self)

    def _add_to_dot(self, dot):
        dot.edge(self._get_dotname(), self.outcome.name, dir="none")

        
OuN = OutcomeNode
"""Abbreviation for OutcomeNode"""


class InformationSet (_AbstractObject):
    """Represents a set of DecisionNodes belonging to the same player 
    which the player cannot distinguish from their information when in one of 
    these DecisionNodes. 
    @param nodes: set of DecisionNodes belonging to this information set.
    All these nodes must have the exact same set of possible named_actions for the
    player.
    """
    
    # TODO: make into a proper iterable!
    
    _i_nodes = None
    @property
    def nodes(self):
        """Set of DecisionNodes, each having its information_set=this"""
        return self._i_nodes

    def __init__(self, name, **kwargs):
        self._i_nodes = []
        super(InformationSet, self).__init__(name, **kwargs)
        for node in self.nodes:
            assert node._i_information_set is None, "node can only be in one information set"
            node._i_information_set = self

    def add_node(self, node):
        if node not in self.nodes:
            assert node._i_information_set is None, "node can only be in one information set" + str(node._i_information_set) + " " + str(self)
            self._i_nodes.append(node)
            node._i_information_set = self
        self.validate()
        
    def validate(self):
        self._i_nodes = list(self.nodes) 
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

    @property
    def choice_history(self):
        """List of (InformationSet, Action) pairs from root to predecessor"""
        return self.nodes[0].choice_history

    def __contains__(self, node):
        return node in self._i_nodes
        
    def __repr__(self):
        return (self.name if hasname(self) else "") + str(tuple(self.nodes))

    def remove_action(self, a):
        """removes an action from all nodes in the set and removes the corr.
        successor's branches from the tree"""
        assert a in self.actions
        assert len(self.actions) > 1, "cannot remove the only action"
        self._a_actions.remove(a)
        for v1 in self.nodes:
            v1.successors.remove(v1.consequences[a])
            v1.consequences[a].remove()
            del v1.consequences[a]

InS = InformationSet
"""Abbreviation for InformationSet"""

def information_sets(*names):
    """Return an InformationSet for each name listed as an argument"""
    return tuple(InformationSet(name) for name in names)
    
inss = information_sets

def global_information_sets(*names):
    """Create an InformationSet for each name listed as an argument 
    and store it in a global variable of the same name"""
    module_name = list(sys._current_frames().values())[0].f_back.f_globals['__name__']
    module = sys.modules[module_name]
    for ins in information_sets(*names):
        n = ins.name
        if getattr(module, n, ins) != ins:
            print("Warning: global var", n, "existed, did not overwrite it.")
        else:
            setattr(module, n, ins)

global_inss = global_information_sets
