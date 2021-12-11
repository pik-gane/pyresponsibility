"""Backward Responsibility Functions based on the idea of backward elimination
of Pareto-dominated actions.
"""

from ..nodes import * 
from ..functions import *

def strictly_dominates(a1, a2, ins):
    """Whether action 1 strictly dominates action 2 in information_set
    w.r.t. all sets of not strictly (!) dominated transitions"""
    T = ins.nodes[0].tree
    for v in ins.nodes:
        for tau in get_undominated_transitions(T, v):
            l1 = T._get_expectation(node=v, transitions={**tau, ins: a1}, resolve=Max)
            l2 = T._get_expectation(node=v, transitions={**tau, ins: a2}, resolve=Max)
            assert l1 <= l2 or l1 > l2
            if l1 >= l2:
                return False
    return True

def is_strictly_dominated(action, ins):
    """Whether action is strictly dominated by any other action in information set"""
    for a1 in ins.actions:
        if a1 != action and strictly_dominates(a1, action, ins):
            return True
    return False
              
def get_undominated_transitions(self, node, include_node=False):
    """generate all transition sets in the branch after v that use only 
    not strictly dominated actions"""
    if isinstance(node, DecisionNode) and include_node:
        # yield from concatenation of partial strategies at all successors,
        # each one enriched by the corresponding choice:
        for action, successor in node.consequences.items():
            ins = node.information_set
            if not is_strictly_dominated(action, ins):
                for choices in get_undominated_transitions(self, successor, True):
                    choices[ins] = action
                    yield choices
    elif isinstance(node, InnerNode):
        # yield from cartesian product of strategies at all successors:
        cartesian_product = itertools.product(*(
            get_undominated_transitions(self, successor, True)
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
    elif isinstance(node, LeafNode):
        yield {}
        
def domination_strength(a1, a2, ins):
    """If action 1 weakly dominates action 2, return the "strength" of this
    domination, i.e., the maximal difference in likelihoods
    w.r.t. all sets of not strictly (!) dominated transitions"""
    strength = 0
    T = ins.nodes[0].tree
    for v in ins.nodes:
        for tau in get_undominated_transitions(T, v):
            l1 = T._get_expectation(node=v, transitions={**tau, ins: a1}, resolve=Max)
            l2 = T._get_expectation(node=v, transitions={**tau, ins: a2}, resolve=Max)
            assert l1 <= l2 or l1 > l2
            if l1 > l2: 
                return 0
            strength = max(strength, l2 - l1)
    return strength

def shortfall(action, ins):
    """The maximal domination strength over action at information set, or zero
    if not weakly dominated"""
    return max([domination_strength(a1, action, ins) 
                for a1 in ins.actions if a1 != action])
              
r_bw_elim = PRF("r_bw_elim", function=(
    lambda T, unused_G, v, a: shortfall(a, v.ins)
    ))



if False:
    """not needed:"""
    
    def weakly_dominates(a1, a2, ins):
        """Whether action 1 weakly dominates action 2 in information_set
        w.r.t. all sets of not strictly (!) dominated transitions"""
        found_better = False
        T = ins.nodes[0].tree
        for v in ins.nodes:
            for tau in get_undominated_transitions(T, v):
                l1 = T._get_expectation(node=v, transitions={**tau, ins: a1}, resolve=Max)
                l2 = T._get_expectation(node=v, transitions={**tau, ins: a2}, resolve=Max)
                assert l1 <= l2 or l1 > l2
                if l1 > l2: 
                    return False
                if l1 < l2:
                    found_better = True
        return found_better
    
    def is_weakly_dominated(action, ins):
        """Whether action is weakly dominated by any other action in information set"""
        for a1 in ins.actions:
            if a1 != action and weakly_dominates(a1, action, ins):
                return True
        return False
    
        