"""Backward Responsibility Functions based on the concept of Pareto-dominated actions.
"""

from ...nodes import * 
from ...functions import *
from ...domination import *

def domination_strength(T, a1, a2, ins):
    """If action 1 weakly dominates action 2, return the "strength" of this
    domination, i.e., the maximal difference in likelihoods
    w.r.t. all sets of not strictly (!) dominated transitions"""
    strength = 0
    for v in ins.nodes:
        for tau in T._get_transitions(node=v, exclude_types=(ProbabilityNode,), 
                                      exclude_group=[], exclude_nodes=[v]):
            l1 = T._get_expectation(node=v, transitions={**tau, ins: a1}, resolve=Max)
            l2 = T._get_expectation(node=v, transitions={**tau, ins: a2}, resolve=Max)
            assert l1 <= l2 or l1 > l2
            if l1 > l2: 
                return 0
            strength = max(strength, l2 - l1)
    return strength

def shortfall(tree, action, ins):
    """The maximal domination strength over action at information set, or zero
    if not weakly dominated"""
    T = tbrt(tree, ins)
    action = T.subs[action]
    ins = T.subs[ins]
    return max([domination_strength(T, a1, action, ins) 
                for a1 in ins.actions if a1 != action])
              
r_stbr = PRF("r_stbr",
             desc="shortfall in trust-based-reduced tree",
             function=(
                lambda T, unused_G, v, a: shortfall(T, a, v.ins)
    ))


        