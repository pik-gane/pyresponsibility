import itertools
import sympy as sp

from .core import update_consistently
from .players import Group
from .solutions import PartialSolution, Scenario, Strategy
from . import nodes

class Branch (object):
    
    _i_root_node = None
    @property
    def root_node(self): 
        return self._i_root_node
    
    def __init__(self, root_node):
        self._i_root_node = root_node
    
    # properties holding dicts of objects keyed by their name:
    
    _a_nodes = None
    @property
    def nodes(self):
        if self._a_nodes is None:
            self._a_nodes = {self.root_node.name: self.root_node} 
            if hasattr(self.root_node, 'successors'):
                for v in self.root_node.successors:
                    self._a_nodes.update(v.branch.nodes)
        return self._a_nodes

    _a_players = None
    @property
    def players(self):
        if self._a_players is None:
            self._a_players = {
                v.player.name: v.player 
                for v in self.nodes.values() if hasattr(v, "player")}
        return self._a_players
    
    _a_outcomes = None
    @property
    def outcomes(self):
        if self._a_outcomes is None:
            self._a_outcomes = {
                v.outcome.name: v.outcome 
                for v in self.nodes.values() if hasattr(v, "outcome")}
        return self._a_outcomes
        
    _a_inner_nodes = None
    @property
    def inner_nodes(self):
        if self._a_inner_nodes is None:
            self._a_inner_nodes = {n: v
                for n, v in self.nodes.items() 
                if isinstance(v, nodes.InnerNode)} 
        return self._a_inner_nodes
        
    _a_possibility_nodes = None
    @property
    def possibility_nodes(self):
        if self._a_possibility_nodes is None:
            self._a_possibility_nodes = {n: v
                for n, v in self.nodes.items() 
                if isinstance(v, nodes.PossibilityNode)} 
        return self._a_possibility_nodes
        
    _a_probability_nodes = None
    @property
    def probability_nodes(self): 
        if self._a_probability_nodes is None:
            self._a_probability_nodes = {n: v
                for n, v in self.nodes.items() 
                if isinstance(v, nodes.ProbabilityNode)} 
        return self._a_probability_nodes

    _a_decision_nodes = None
    @property
    def decision_nodes(self): 
        if self._a_decision_nodes is None:
            self._a_decision_nodes = {n: v
                for n, v in self.nodes.items() 
                if isinstance(v, nodes.DecisionNode)} 
        return self._a_decision_nodes

    _a_leaf_nodes = None
    @property
    def leaf_nodes(self):
        if self._a_leaf_nodes is None:
            self._a_leaf_nodes = {n: v
                for n, v in self.nodes.items() 
                if isinstance(v, nodes.LeafNode)} 
        return self._a_leaf_nodes
        
    _a_outcome_nodes = None
    @property
    def outcome_nodes(self): 
        if self._a_outcome_nodes is None:
            self._a_outcome_nodes = {n: v
                for n, v in self.nodes.items() 
                if isinstance(v, nodes.OutcomeNode)} 
        return self._a_outcome_nodes

    _a_decision_nodes_d = {}
    def get_decision_nodes(self, player_or_group):
        if player_or_group not in self._a_decision_nodes_d:
            self._a_decision_nodes_d[player_or_group] = {n: v
                for n, v in self.decision_nodes.items() 
                if v.player == player_or_group 
                or (isinstance(player_or_group, Group) 
                    and v.player in player_or_group)} 
        return self._a_decision_nodes_d[player_or_group]

    _a_information_sets_d = {}
    def get_information_sets(self, player):
        if player not in self._a_information_sets_d:
            self._a_information_sets_d[player] = {
                v.information_set.name: v.information_set
                for v in self.get_decision_nodes(player).values()} 
        return self._a_information_sets_d[player]

    _a_actions = None
    @property
    def actions(self):
        if self._a_actions is None:
            self._a_actions = {a.name: a
                for v in self.nodes.values() if hasattr(v, "actions")
                for a in v.actions}
        return self._a_actions
        
    # generators for solutions:
    
    def _get_transitions(self, node=None, include_types=None, exclude_types=None, 
                         include_group=None, exclude_group=None, consistently=None):
        if (( # type is selected:
             (include_types is not None and isinstance(node, include_types)) 
             or (exclude_types is not None and not isinstance(node, exclude_types))
            )
            and 
            ( # if decision node, player is selected:
             not isinstance(node, nodes.DecisionNode) 
             or (include_group is not None and node.player in include_group)
             or (exclude_group is not None and node.player not in exclude_group)
            )):
            # yield from concatenation of partial solutions of all successors,
            # each one enriched by the corresponding transition:
            if (consistently and isinstance(node, nodes.DecisionNode)):
                for action in node.actions:
                    for transitions in self._get_transitions(
                            node=node.consequences[action], include_types=include_types, exclude_types=exclude_types, 
                            include_group=include_group, exclude_group=exclude_group, consistently=consistently):
                        transitions[node.information_set] = action
                        yield transitions
            else:
                for successor in node.successors:
                    for transitions in self._get_transitions(
                            node=successor, include_types=include_types, exclude_types=exclude_types, 
                            include_group=include_group, exclude_group=exclude_group, consistently=consistently):
                        transitions[node] = successor
                        yield transitions
        elif isinstance(node, nodes.InnerNode):
            # yield from cartesian product of strategies of all successors:
            cartesian_product = itertools.product(*(
                self._get_transitions(
                    node=successor, include_types=include_types, exclude_types=exclude_types, 
                    include_group=include_group, exclude_group=exclude_group, consistently=consistently)
                for successor in node.successors))
            for combination in cartesian_product:
                transitions = {}
                is_ok = True
                for component in combination:
                    if consistently: 
                        is_ok = is_ok and update_consistently(transitions, component)
                        if not is_ok: break
                    else:
                        transitions.update(component)
                if is_ok:
                    yield transitions
        elif isinstance(node, nodes.LeafNode):
            yield {}
    
    def get_partial_solutions(self, node=None, include_types=None, exclude_types=None, 
                              include_group=None, exclude_group=None, consistently=None):
        assert isinstance(node, nodes.Node)
        if include_types is not None:
            assert exclude_types is None, "either specify include_types or exclude_types"
            for ty in include_types:
                assert issubclass(ty, nodes.InnerNode)
        else:
            assert exclude_types is not None, "either specify include_types or exclude_types"
            for ty in exclude_types:
                assert issubclass(ty, nodes.InnerNode)
        if include_group is not None:
            assert exclude_group is None, "you cannot specify both include_group or exclude_group"
            assert isinstance(include_group, Group)
        elif ((include_types is not None and nodes.DecisionNode in include_types) 
              or (exclude_types is not None and nodes.DecisionNode not in exclude_types)):
            assert exclude_group is not None, "either specify include_group or exclude_group"
            assert isinstance(exclude_group, Group) 
        assert isinstance(consistently, bool)
        for transitions in self._get_transitions(
                node=node, include_types=include_types, exclude_types=exclude_types, 
                include_group=include_group, exclude_group=exclude_group, consistently=consistently):
            yield PartialSolution("_", transitions=transitions)
        
    def get_scenarios(self, node=None, player=None, group=None):
        if player:
            assert group is None
            group = Group("_", players={player})
        assert isinstance(group, Group)
        if isinstance(node, nodes.DecisionNode):
            assert node.player in group
            # yield from concatenation of scenarios of all nodes in same information set:
            nodes = node.information_set.nodes
        else:
            nodes = {node}
        for v in node.information_set.nodes: 
            for transitions in self._get_transitions(
                    node=v, include_types=(nodes.PossibilityNode, nodes.DecisionNode), 
                    exclude_group=group, consistently=True):
                yield Scenario("_", anchor=v, transitions=transitions)
    
    def _get_choices(self, node=None, group=None):
        if isinstance(node, nodes.DecisionNode) and node.player in group:
            # yield from concatenation of partial strategies at all successors,
            # each one enriched by the corresponding choice:
            for action in node.actions:
                for choices in self._get_choices(node=node.consequences[action], group=group):
                    choices[node.information_set] = action
                    yield choices
        elif isinstance(node, nodes.InnerNode):
            # yield from cartesian product of strategies at all successors:
            cartesian_product = itertools.product(*(
                self._get_choices(node=successor, group=group)
                for successor in node.successors))
            for combination in cartesian_product:
                choices = {}
                is_consistent = True
                for component in combination:
                    is_consistent = is_consistent and update_consistently(choices, component)
                    if not is_consistent: break
                if is_consistent: yield choices
        elif isinstance(node, nodes.LeafNode):
            yield {}
        
    def get_strategies(self, node=None, player=None, group=None):
        assert isinstance(node, nodes.Node)
        if player:
            assert group is None
            group = Group("_", players={player})
        assert isinstance(group, Group)
        if isinstance(node, nodes.DecisionNode):
            assert node.player in group
            # yield from cartesian product of strategies of all nodes in same information set:
            nodes = node.information_set.nodes
        else:
            nodes = {node}
        cartesian_product = itertools.product(*(
            self._get_choices(node=v, group=group)
            for v in nodes))
        for combination in cartesian_product:
            choices = {}
            is_consistent = True
            for component in combination:
                is_consistent = is_consistent and update_consistently(choices, component)
                if not is_consistent: break
            if is_consistent: yield Strategy("_", anchor=node, choices=choices)
        
    # outcome distributions:
        
    def _get_outcome_distribution(self, node=None, transitions=None):
        if isinstance(node, nodes.OutcomeNode):
            return {node.outcome: 1}
        elif not isinstance(node, nodes.ProbabilityNode):
            successor = transitions[node] if node in transitions else node.consequences[transitions[node.information_set]]
            return self._get_outcome_distribution(successor, transitions)
        else:
            distribution = {}
            for successor, p1 in node.probabilities.items():
                for outcome, p2 in self._get_outcome_distribution(successor, transitions).items():
                    p = distribution.get(outcome, 0) + p1*p2
                    if isinstance(p, sp.Expr):
                        p = sp.simplify(p)
                    distribution[outcome] = p
            return distribution
            
    def get_outcome_distribution(self, scenario=None, strategy=None):
        assert isinstance(scenario, Scenario)
        assert isinstance(strategy, Strategy)
        transitions = scenario.transitions
        for ins, act in strategy.choices.items():
            assert ins not in transitions, "scenario and strategy must not overlap"
            transitions[ins] = act
        return self._get_outcome_distribution(node=self.root_node, transitions=transitions)
