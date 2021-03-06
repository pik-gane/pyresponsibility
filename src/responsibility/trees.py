import sys
import itertools
import numpy as np
import sympy as sp
try:
    import graphviz as gv
except:
    print("Branch.draw() unavailable since graphviz python package is not available")

from .core import _AbstractObject, hasname, update_consistently, profile, Max, Min
from .players import Group, _get_group
from .solutions import PartialSolution, Scenario, Strategy
from . import nodes as nd

"""
References:
[AAFRA] Hiller, S., Israel, J., & Heitzig, J. (2021). An Axiomatic Approach to Formalized Responsibility Ascription.
"""

class Branch (_AbstractObject):
    """Represents that part of the tree that starts at some anchor node that
    serves as the branch's "root".
    @param root: the node serving as the branch's root 
           (not necessarily the root of the whole tree)
           
    This class also provides many methods to be used in responsibility calculations,
    e.g. to find all players, outcomes, nodes, or information sets occurring in
    this branch, find all scenarios or strategies starting at the branch's root node,
    or to find the outcome distribution resulting from a scenario-strategy pair.
    """
    
    _i_root = None
    @property
    def root(self): 
        return self._i_root
    
    def __init__(self, *args, total_recall=True, **kwargs):
        super(Branch, self).__init__(*args, **kwargs)
        if total_recall:
            # assert that nodes in the same information set have the same choice_history:
            for ins in self.get_information_sets():
                if len(ins.nodes) > 1:
                    hist = ins.nodes[0].choice_history
                    for v in ins.nodes[1:]:
                        if not v.choice_history == hist:
                            if v.choice_history != hist:
                                print(
#                            assert v.choice_history == hist, 
                                "nodes " + str(ins.nodes[0]) + " and " + str(v) + " have a different choice history!"
                                )
                                print(v.choice_history, hist)
                                print(repr(self))
                                print()
        
    def clone(self, name=None, desc=None, subs=None, keep=None):
        """Return a deep copy of this branch as an independent Tree with 
        no connections to this tree"""
        if subs is None:
            subs = {}
        return Tree((name if name is not None else "clone_of_" + self.name),
                    desc=(desc if desc is not None else self.desc), 
                    ro=self.root.clone(subs=subs, keep=keep), 
                    subs=subs) 
        
    # properties holding dicts of named objects keyed by their name:
    
    _a_named_nodes = None
    @property
    def named_nodes(self):
        """dict of named nodes keyed by name"""
        if self._a_named_nodes is None:
            self._a_named_nodes = {self.root.name: self.root} if hasname(self.root) else {} 
            if hasattr(self.root, 'successors'):
                for v in self.root.successors:
                    self._a_named_nodes.update(v.branch.named_nodes)
        return self._a_named_nodes

    _a_named_inner_nodes = None
    @property
    def named_inner_nodes(self):
        if self._a_named_inner_nodes is None:
            self._a_named_inner_nodes = {n: v
                for n, v in self.named_nodes.items() 
                if isinstance(v, nd.InnerNode)} 
        return self._a_named_inner_nodes
        
    _a_named_possibility_nodes = None
    @property
    def named_possibility_nodes(self):
        if self._a_named_possibility_nodes is None:
            self._a_named_possibility_nodes = {n: v
                for n, v in self.named_nodes.items() 
                if isinstance(v, nd.PossibilityNode)} 
        return self._a_named_possibility_nodes
        
    _a_named_probability_nodes = None
    @property
    def named_probability_nodes(self): 
        if self._a_named_probability_nodes is None:
            self._a_named_probability_nodes = {n: v
                for n, v in self.named_nodes.items() 
                if isinstance(v, nd.ProbabilityNode)} 
        return self._a_named_probability_nodes

    _a_named_decision_nodes = None
    @property
    def named_decision_nodes(self): 
        if self._a_named_decision_nodes is None:
            self._a_named_decision_nodes = {n: v
                for n, v in self.named_nodes.items() 
                if isinstance(v, nd.DecisionNode)} 
        return self._a_named_decision_nodes

    _a_named_players = None
    @property
    def named_players(self):
        """dict of named named_players keyed by name"""
        if self._a_named_players is None:
            self._a_named_players = {
                v.player.name: v.player 
                for v in self.get_nodes() 
                if hasattr(v, "player") and hasname(v.player)}
        return self._a_named_players
    
    _a_named_outcomes = None
    @property
    def named_outcomes(self):
        """dict of named named_outcomes keyed by name"""
        if self._a_named_outcomes is None:
            self._a_named_outcomes = {
                v.outcome.name: v.outcome 
                for v in self.get_nodes() 
                if hasattr(v, "outcome") and hasname(v.outcome)}
        return self._a_named_outcomes
        
    _a_named_leaf_nodes = None
    @property
    def named_leaf_nodes(self):
        if self._a_named_leaf_nodes is None:
            self._a_named_leaf_nodes = {n: v
                for n, v in self.named_nodes.items() 
                if isinstance(v, nd.LeafNode)} 
        return self._a_named_leaf_nodes
        
    _a_named_outcome_nodes = None
    @property
    def named_outcome_nodes(self): 
        if self._a_named_outcome_nodes is None:
            self._a_named_outcome_nodes = {n: v
                for n, v in self.named_nodes.items() 
                if isinstance(v, nd.OutcomeNode)} 
        return self._a_named_outcome_nodes

    _a_named_information_sets = None
    @property
    def named_information_sets(self):
        """dict of named named_information_sets keyed by name"""
        if self._a_named_information_sets is None:
            self._a_named_information_sets = {
                v.information_set.name: v.information_set
                for v in self.named_decision_nodes.values()
                if hasname(v.information_set)} 
        return self._a_named_information_sets

    _a_named_actions = None
    @property
    def named_actions(self):
        if self._a_named_actions is None:
            self._a_named_actions = {a.name: a
                for v in self.named_nodes.values() if hasattr(v, "actions")
                for a in v.actions}
        return self._a_named_actions

    _a_named_symbols = None
    @property    
    def named_symbols(self):
        """dict of all symbols occurring in probabilities"""
        if self._a_named_symbols is None:
            self._a_named_symbols = {}
            for v in self.get_probability_nodes():
                for p in v.probabilities.values():
                    if isinstance(p, sp.Expr):
                        self._a_named_symbols.update({
                            s.name: s 
                            for s in p.free_symbols
                        }) 
        return self._a_named_symbols

    _a_players = None
    @property    
    def players(self):
        """set of all (!) players, named or not"""
        if self._a_players is None:
            self._a_players = {v.player for v in self.get_decision_nodes()}
        return self._a_players

    # generators for objects, named or not:
        
    def get_nodes(self):
        """yield all (!) nodes, named or not"""
        yield self.root
        if hasattr(self.root, 'successors'):
            for v in self.root.successors:
                for v2 in v.branch.get_nodes():
                    yield v2

    def get_inner_nodes(self):
        """yield all (!) inner nodes, named or not"""
        for v in self.get_nodes():
            if isinstance(v, nd.InnerNode):
                yield v 

    def get_possibility_nodes(self):
        """yield all (!) possibility nodes, named or not"""
        for v in self.get_nodes():
            if isinstance(v, nd.PossibilityNode):
                yield v 

    def get_probability_nodes(self):
        """yield all (!) probability nodes, named or not"""
        for v in self.get_nodes():
            if isinstance(v, nd.ProbabilityNode):
                yield v 

    def get_decision_nodes(self, player_or_group=None):
        """yield all (!) decision nodes, named or not, optionally restricted
        to those of a certain player or group"""
        for v in self.get_nodes():
            if isinstance(v, nd.DecisionNode) and (
                    player_or_group is None
                    or v.player == player_or_group 
                    or (isinstance(player_or_group, Group) 
                        and v.player in player_or_group)):
                yield v 

    def get_leaf_nodes(self):
        """yield all (!) leaf nodes, named or not"""
        for v in self.get_nodes():
            if isinstance(v, nd.LeafNode):
                yield v 

    def get_outcome_nodes(self):
        """yield all (!) outcome nodes, named or not"""
        for v in self.get_nodes():
            if isinstance(v, nd.OutcomeNode):
                yield v 

    def get_information_sets(self, player_or_group=None):
        """yield all (!) information sets, named or not, optionally restricted
        to those of a certain player or group"""
        for v in self.get_decision_nodes(player_or_group):
            ins = v.information_set
            if ins.nodes[0] == v:
                yield ins

    def get_outcomes(self):
        """yield all (!) outcomes, named or not"""
        for v in self.get_outcome_nodes():
            ou = v.outcome
            if ou.nodes[0] == v:
                yield ou
            
    # generators for solutions:
    
    #@profile
    def _get_transitions(self, node=None, include_types=None, exclude_types=None, 
                         include_group=None, exclude_group=None, consistently=None,
                         fixed_transitions=None, exclude_nodes=None):
        """helper function"""
        if fixed_transitions is None:
            fixed_transitions = {}
        if exclude_nodes is None:
            exclude_nodes = []
        if isinstance(node, nd.InnerNode):
            if (node not in exclude_nodes
                and
                ( # type is selected:
                 (include_types is not None and isinstance(node, include_types)) 
                 or (exclude_types is not None and not isinstance(node, exclude_types))
                )
                and 
                ( # if decision node, player is selected:
                 not isinstance(node, nd.DecisionNode) 
                 or (include_group is not None and node.player in include_group)
                 or (exclude_group is not None and node.player not in exclude_group)
                )):
                # yield from concatenation of partial solutions of all successors,
                # each one enriched by the corresponding transition:
                if (consistently and isinstance(node, nd.DecisionNode)):
                    ins = node.information_set
                    if ins in fixed_transitions:
                        action = fixed_transitions[ins]
                        successor = node.consequences[action]
                        for transitions in self._get_transitions(
                                node=successor, include_types=include_types, exclude_types=exclude_types, 
                                include_group=include_group, exclude_group=exclude_group, consistently=consistently):
                            transitions[ins] = action
                            yield transitions
                    elif node in fixed_transitions:
                        successor = fixed_transitions[node]
                        for transitions in self._get_transitions(
                                node=successor, include_types=include_types, exclude_types=exclude_types, 
                                include_group=include_group, exclude_group=exclude_group, consistently=consistently):
                            transitions[node] = successor
                            yield transitions                    
                    else:                    
                        for action, successor in node.consequences.items():
                            for transitions in self._get_transitions(
                                    node=successor, include_types=include_types, exclude_types=exclude_types, 
                                    include_group=include_group, exclude_group=exclude_group, consistently=consistently):
                                transitions[ins] = action
                                yield transitions
                else:
                    for successor in node.successors:
                        for transitions in self._get_transitions(
                                node=successor, include_types=include_types, exclude_types=exclude_types, 
                                include_group=include_group, exclude_group=exclude_group, consistently=consistently):
                            transitions[node] = successor
                            yield transitions
            else:
                # yield from cartesian product of strategies of all successors:
                su = [fixed_transitions[node]] if node in fixed_transitions else node.successors
                cartesian_product = itertools.product(*(
                    self._get_transitions(
                        node=successor, include_types=include_types, exclude_types=exclude_types, 
                        include_group=include_group, exclude_group=exclude_group, consistently=consistently)
                    for successor in su))
                if consistently: 
                    for combination in cartesian_product:
                        transitions = {}
                        is_ok = True
                        for component in combination:
                            is_ok = update_consistently(transitions, component)
                            if not is_ok: 
                                break
                        if is_ok:
                            yield transitions
                else:
                    for combination in cartesian_product:
                        transitions = {}
                        for component in combination:
                            transitions.update(component)
                        yield transitions
        elif isinstance(node, nd.LeafNode):
            yield {}
    
    def get_partial_solutions(self, node=None, include_types=None, exclude_types=None, 
                              include_group=None, exclude_group=None, consistently=None):
        """helper method"""
        assert isinstance(node, nd.Node)
        if include_types is not None:
            assert exclude_types is None, "either specify include_types or exclude_types"
            for ty in include_types:
                assert issubclass(ty, nd.InnerNode)
        else:
            assert exclude_types is not None, "either specify include_types or exclude_types"
            for ty in exclude_types:
                assert issubclass(ty, nd.InnerNode)
        if include_group is not None:
            assert exclude_group is None, "you cannot specify both include_group or exclude_group"
            assert isinstance(include_group, Group)
        elif ((include_types is not None and nd.DecisionNode in include_types) 
              or (exclude_types is not None and nd.DecisionNode not in exclude_types)):
            assert exclude_group is not None, "either specify include_group or exclude_group"
            assert isinstance(exclude_group, Group) 
        assert isinstance(consistently, bool)
        for transitions in self._get_transitions(
                node=node, include_types=include_types, exclude_types=exclude_types, 
                include_group=include_group, exclude_group=exclude_group, consistently=consistently):
            yield PartialSolution("_", transitions=transitions)
        
    def get_scenarios(self, node=None, player=None, group=None, fixed_transitions=None):
        """Return all scenarios for the given player or group starting at some 
        node, potentially restricted to the optional dict of fixed_transitions.
        @return: generator for Scenario objects   
        """
        if fixed_transitions is None:
            fixed_transitions = {}
        group = _get_group(player=player, group=group)
        assert group is not None
        if isinstance(node, nd.DecisionNode) and node.player in group:
            # yield from concatenation of scenarios of all nodes in same information set:
            nodes = node.information_set.nodes
        else:
            nodes = {node}
        for v in nodes: 
            for transitions in self._get_transitions(
                    node=v, include_types=(nd.PossibilityNode, nd.DecisionNode), 
                    exclude_group=group, consistently=True, fixed_transitions=fixed_transitions):
                yield Scenario("_", current_node=v, transitions=transitions)
    
    #@profile
    def _get_choices(self, node=None, group=None, fixed_choices=None):
        """helper method"""
        if fixed_choices is None:
            fixed_choices = {}
        if isinstance(node, nd.DecisionNode) and node.player in group:
            # yield from concatenation of partial strategies at all successors,
            # each one enriched by the corresponding choice:
            ins = node.information_set
            if ins in fixed_choices:
                action = fixed_choices[ins]
                successor = node.consequences[action]
                for choices in self._get_choices(node=successor, group=group, fixed_choices=fixed_choices):
                    choices[ins] = action
                    yield choices
            else:                    
                for action, successor in node.consequences.items():
                    for choices in self._get_choices(node=successor, group=group, fixed_choices=fixed_choices):
                        choices[ins] = action
                        yield choices
        elif isinstance(node, nd.InnerNode):
            # yield from cartesian product of strategies at all successors:
            cartesian_product = itertools.product(*(
                self._get_choices(node=successor, group=group, fixed_choices=fixed_choices)
                for successor in node.successors))
            for combination in cartesian_product:
                choices = {}
                is_consistent = True
                for component in combination:
                    is_consistent = update_consistently(choices, component)
                    if not is_consistent: 
                        break
                if is_consistent: 
                    yield choices
        elif isinstance(node, nd.LeafNode):
            yield {}
        
    def get_strategies(self, node=None, player=None, group=None, fixed_choices=None):
        """Return all strategies for the given player or group starting at a 
        certain node, potentially restricted to matching the optionally specified
        dict of fixed_choices. 
        @return: generator for Strategy objects   
        """
        if fixed_choices is None:
            fixed_choices = {}
        assert isinstance(node, nd.Node)
        group = _get_group(player=player, group=group)
        assert group is not None
        if isinstance(node, nd.DecisionNode) and node.player in group:  
            # yield from basically the cartesian product of strategies of all nodes in same information set:
            ins = node.information_set
            combinations = itertools.chain(*(itertools.product(*(
                    self._get_choices(node=v, group=group, fixed_choices={**fixed_choices, ins: a})
                    for v in ins.nodes))
                for a in ([fixed_choices[ins]] if ins in fixed_choices else ins.actions)))
        else:
            combinations = itertools.product(self._get_choices(node=v, group=group, fixed_choices=fixed_choices))
        for combination in combinations:
            choices = {}
            is_consistent = True
            for component in combination:
                is_consistent = is_consistent and update_consistently(choices, component)
                if not is_consistent: 
                    break
            if is_consistent: 
                yield Strategy("_", choices=choices)
        
    # outcome distributions:
        
    _n_not_used_cache = 0
    _n_used_cache = 0
    
    _d_outcome_distribution = {}
    #@profile
    def _get_outcome_distribution(self, node=None, transitions=None):
        """helper method"""
        if isinstance(node, nd.OutcomeNode):
            return {node.outcome: 1}
        elif not isinstance(node, nd.ProbabilityNode):
            new_transitions = transitions.copy()
            if node in transitions:
                successor = new_transitions.pop(node) 
            else:
                successor = node.consequences[new_transitions.pop(node.information_set)]
            return self._get_outcome_distribution(successor, new_transitions)
        else:
            key = (node, frozenset(transitions.items()))
            try:
                distribution = self._d_outcome_distribution[key]
                self._n_used_cache += 1
                return distribution
            except:
                self._n_not_used_cache += 1
                distribution = {}
                for successor, p1 in node.probabilities.items():
                    for outcome, p2 in self._get_outcome_distribution(successor, transitions).items():
                        distribution[outcome] = distribution.get(outcome, 0) + p1*p2
                self._d_outcome_distribution[key] = distribution
                return distribution
            
    def get_outcome_distribution(self, node=None, scenario=None, strategy=None):
        """Returns the probability of outcomes resulting from a given
        scenario and strategy.
        @return: dict of probability keyed by Outcome
        """
        assert isinstance(node, nd.Node)
        assert isinstance(scenario, Scenario) and node in scenario.current_node.information_set
        assert isinstance(strategy, Strategy)
        transitions = {**scenario.transitions}
        for S, act in strategy.choices.items():
            assert S not in transitions, "scenario and strategy must not overlap"
            transitions[S] = act
        distribution = self._get_outcome_distribution(node=scenario.current_node, transitions=transitions)
        for (ou, p) in distribution.items():
            if isinstance(p, sp.Expr):
                distribution[ou] = sp.simplify(p)
        return distribution

    def _get_expectation(self, node=None, transitions=None, attribute=None, resolve=None):
        """helper method"""
        if isinstance(node, nd.OutcomeNode):
            return ((0 if node.outcome.is_acceptable else 1) if attribute is None 
                    else getattr(node.outcome, attribute, 0))
        elif isinstance(node, nd.ProbabilityNode):
            expectation = 0
            for successor, p1 in node.probabilities.items():
                expectation += p1 * self._get_expectation(successor, transitions, attribute, resolve)
            return expectation
        else:
            if node in transitions:
                successor = transitions[node]
                return self._get_expectation(successor, transitions, attribute, resolve)
            elif isinstance(node, nd.DecisionNode):
                ins = node.information_set
                if ins in transitions:
                    successor = node.consequences[transitions[ins]]
                    return self._get_expectation(successor, transitions, attribute, resolve)
        return resolve([self._get_expectation(successor, transitions, attribute, resolve)
                        for successor in node.successors])
    
    def get_expectation(self, node=None, scenario=None, player=None, group=None,
                        strategy=None, attribute=None, resolve=None):
        """Calculate the (min or max) expectation value of some outcome attribute
        conditional on being in the branch's root node and optionally assuming 
        a certain scenario and strategy.
        @param attribute: name of the outcome attribute
        @param resolve: whether to use the Min or Max expectation over those
               decision and possiblity nodes not resolved by scenario and strategy
        @param player, group: if node player equals player or is in group and no 
               strategy is given, we assume the uncertainty implied by the node's
               information set. 
        If the outcome lacks the attribute, a zero value is assumed.
        """
        assert isinstance(node, nd.Node)
        assert isinstance(attribute, str)
        if scenario is not None:
            assert isinstance(scenario, Scenario)
            transitions = {**scenario.transitions}
            if strategy is not None:
                assert isinstance(strategy, Strategy)
                for S, act in strategy.choices.items():
                    assert S not in transitions, "scenario and strategy must not overlap"
                    transitions[S] = act
            expectation = self._get_expectation(scenario.current_node, transitions, attribute, resolve)
            return sp.simplify(expectation) if isinstance(expectation, sp.Expr) else expectation
        else:
            if isinstance(node, nd.DecisionNode):
                group = _get_group(player=player, group=group)
                assert group is not None
                nodes = node.information_set.nodes if node.player in group else {node} 
            else:
                nodes = {node}
            # take min or max over relevant nodes:
            return resolve([self._get_expectation(
                                node=node, scenario=Scenario("", current_node=c, transitions={}), 
                                strategy=strategy, attribute=attribute, resolve=resolve)
                            for c in nodes])
        
    def get_likelihood(self, node=None, scenario=None, player=None, group=None,
                       strategy=None, is_acceptable=False, resolve=None):
        """Calculate the (min or max) probability of an unacceptable (or acceptable) outcome
        conditional on being in the branch's root node and optionally assuming 
        a certain scenario and strategy.
        @param is_acceptable: whether the probability of unacceptable (False) or acceptable (True)
               outcomes is sought (default: False)
        @param resolve: whether to use the Min or Max probability over those
               decision and possibility nodes not resolved by scenario and strategy
        @param player, group: if node player equals player or is in group and no 
               strategy is given, we assume the uncertainty implied by the node's
               information set. 
        """
        assert isinstance(node, nd.Node)
        assert isinstance(is_acceptable, bool)
        if scenario is not None:
            assert isinstance(scenario, Scenario)
            transitions = {**scenario.transitions}
            if strategy is not None:
                assert isinstance(strategy, Strategy)
                for S, act in strategy.choices.items():
                    assert S not in transitions, "scenario and strategy must not overlap"
                    transitions[S] = act
            likelihood = self._get_expectation(scenario.current_node, transitions, None, resolve)
            return sp.simplify(likelihood) if isinstance(likelihood, sp.Expr) else likelihood
        else:
            if isinstance(node, nd.DecisionNode):
                group = _get_group(player=player, group=group)
                assert group is not None
                nodes = node.information_set.nodes if node.player in group else {node} 
            else:
                nodes = {node}
            # take min or max over relevant nodes:
            return resolve([self.get_likelihood(
                                node=c, scenario=Scenario("", current_node=c, transitions={}), 
                                strategy=strategy, is_acceptable=is_acceptable, resolve=resolve)
                            for c in nodes])
    
    # some useful components for constructing responsibility functions:
    
    def get_guaranteed_likelihood(self, player=None, group=None, node=None):
        """Calculate the known guaranteed likelihood (minimum likelihood over
        all scenario and strategies) of an unacceptable outcome, called gamma in AAFRA"""
        return self.get_likelihood(node=node, scenario=None, player=player, group=group, strategy=None, resolve=Min)

    gamma = get_guaranteed_likelihood

    def get_optimal_avoidance_likelihood(self, node=None, scenario=None):
        """Calculate the minimal likelihood achievable by the "optimal avoidance" strategy given
        a certain scenario, called omega in AAFRA"""
        return self.get_likelihood(node=node, scenario=scenario, strategy=None, resolve=Min)

    omega = get_optimal_avoidance_likelihood
    
    def Delta_omega(self, node=None, scenario=None, action=None):
        """Shortfall in minimizing likelihood: by how much has the minimally 
        achievable likelihood in the given scenario increased from this node 
        to the next due to taking the given action? See AAFRA""" 
        return (self.omega(node=node.consequences[action], 
                           scenario=scenario.sub_scenario(action)) 
                - self.omega(node=node, scenario=scenario))
                
    def rho(self, group=None, node=None, action=None):
        """Risk taken when taking a certain action in a certain node,
        given a certain scenario. See AAFRA"""
        return Max([self.Delta_omega(node=node, scenario=scenario, action=action)
                    for scenario in self.get_scenarios(node=node, group=group)])
                    
    def rho_min(self, group=None, node=None):
        """Minimal risk in node. See AAFRA"""
        return Min([self.rho(group=group, node=node, action=action)
                    for action in node.actions])
                    
    def cooperatively_achievable_likelihood(self, node=None, env_scenario=None, fixed_choices=None):
        """Achievable likelihood of unacceptable outcome under a certain env_scenario
        for all possibility nodes, minimized over all joint strategies of the whole 
        player set that respect the optionally given fixed_choices.
        """
        if fixed_choices is None:
            fixed_choices = {}
        assert isinstance(env_scenario, Scenario)
        all = Group("all", players=self.players)
        res = Min([
            self.get_likelihood(node=node, scenario=env_scenario, strategy=strategy, resolve=Max)
            for strategy in self.get_strategies(node=node, group=all, fixed_choices=fixed_choices)
        ])
        return res

    def cooperatively_achievable_worst_case_likelihood(self, node=None, fixed_choices=None):
        """Minimum of worst-case likelihood of unacceptable outcome,
        minimized over all joint strategies of the whole player set that respect
        the optionally given fixed_choices.
        """
        if fixed_choices is None: 
            fixed_choices = {}
        all = Group("all", players=self.players)
        return Min([
            self.get_likelihood(node=node, group=all, strategy=strategy, resolve=Max)
            for strategy in self.get_strategies(node=node, group=all)
            if strategy.includes(fixed_choices)
        ])

    # other methods_

    def __repr__(self):
        """Returns a multi-line half-graphical representation of the tree.
        Each node is one line, connected by lines indicating successor relationships.
        Actions and probabilities are named right before the node they lead to.
        Non-singleton information sets are named in parentheses after node names.
        Players of decision nodes and outcomes of outcome nodes are named after a colon after node names.
        Acceptable outcomes are marked by a check mark, inacceptable ones by a cross.
        Unnamed nodes are represented by a bullet. 
        @return: str (multiline)
        """
        return self.name + ":" + self.root._to_lines("", "")

    def draw(self, filename, show=False):
        """Draw the tree using graphviz and potentially show it.
        Possibility nodes are diamonds with optionally labeled outgoing arrows, 
        decision nodes are diamonds with player names and arrows labeled by actions,
        probability nodes are squares with arrows labeled by probabilities,
        outcome nodes are circles,
        acceptable and inacceptable outcomes are upward- and downward-pointing triangles,
        information sets are dashed boxes.
        """
        dot = gv.Digraph(comment=self.name, graph_attr={
                "rankdir": "LR",
                "labeldistance": "100.0"})
        with dot.subgraph(name="cluster_outcome_nodes", graph_attr={"style": "invis"}) as sub:
            for w in self.get_outcome_nodes():
                nd.Node._add_to_dot(w, sub)
        with dot.subgraph(name="cluster_outcomes", graph_attr={"style": "invis"}) as sub:
            for ou in self.get_outcomes():
                sub.node(ou.name, shape="triangle" if ou.is_acceptable else "invtriangle")
        self.root._add_to_dot(dot)
        dot.render(outfile=filename, view=show)


class Tree (Branch):
    """Represents the whole tree (=the branch starting at the tree's root node)"""
    
    _i_substitutions = None
    @property
    def substitutions(self):
        """Dict of substitutions made when producing this tree."""
        return self._i_substitutions
        
    subs = substitutions
    
    def validate(self):
        assert self.root.predecessor is None
        # TODO: make sure all node names and ins names are distinct!
        
    def clone_constrained(self, name=None, desc=None, subs=None, information_set=None):
        """Return a clone that contains only those parts which are
        consistent with information_set"""
        keep = set()
        for v in information_set.nodes:
            keep.update(v.path)
            keep.update([*v.branch.get_nodes()])
        return self.clone(name=name, desc=desc, subs=subs, keep=keep)
        
    def make_globals(self, overwrite=False):
        """In the calling module, make a global variable for each 
        player, action, outcome, node, or information set 
        whose name begins with a letter, unless the global variable already exists."""
        module_name = list(sys._current_frames().values())[0].f_back.f_globals['__name__']
        module = sys.modules[module_name]
        for n, v in {**self.named_nodes, 
                     **self.named_information_sets, 
                     **self.named_players, 
                     **self.named_actions, 
                     **self.named_outcomes,
                     **self.named_symbols}.items():
            if hasname(v):
                if getattr(module, n, v) != v and not overwrite:
                    print("Warning: global var", n, "existed, did not overwrite it.")
                else:
                    setattr(module, n, v)
