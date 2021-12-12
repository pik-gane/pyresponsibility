from .core import Min, Max
from .nodes import * 
from .trees import *

def strictly_dominates(a1, a2, ins):
    """Whether action 1 strictly dominates action 2 in information_set"""
    T = ins.nodes[0].tree
    for v in ins.nodes:
        for tau in T._get_transitions(node=v, exclude_types=(ProbabilityNode,), 
                                      exclude_group=[], exclude_nodes=[v]):
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
              
def weakly_dominates(a1, a2, ins):
    """Whether action 1 weakly dominates action 2 in information_set
    w.r.t. all sets of not strictly (!) dominated transitions"""
    found_better = False
    T = ins.nodes[0].tree
    for v in ins.nodes:
        for tau in T._get_transitions(node=v, exclude_types=(ProbabilityNode,), 
                                      exclude_group=[], exclude_nodes=[v]):
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

def trust_based_reduced_tree(tree, information_set):
    """Return a clone of the tree where all nodes incompatible with information
    set and all iteratively strongly dominated future actions that are not in 
    the history of information_set or belong to the information set are removed."""
    ins = information_set
    assert isinstance(ins, InformationSet)
    T = tree.clone_constrained(name="tbrt_of_" + tree.name + "_for_" + ins.name,
                               information_set=ins)
    anchor = T.subs[ins]
    change = True
    while change:
        change = False
        for ins2 in T.get_information_sets():
            if ins2 != anchor:
                for a in [*ins2.actions]:
                    if not (ins2, a) in anchor.choice_history:
                        if is_strictly_dominated(a, ins2):
                            ins2.remove_action(a)
                            change = True
                            ins2._i_name += "'"
            if change:
                break        
    return T
    
tbrt = trust_based_reduced_tree
"""Abbreviation for trust_based_reduced_tree"""

