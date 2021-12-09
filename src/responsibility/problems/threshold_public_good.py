"""n_players players simultaneously either contribute to a public good or don't.
It is only acceptable if at least l contribute.""" 

import itertools

from ..__init__ import *

from sympy import symbols

def threshold_public_good(n_players, threshold):
    """return a Tree for a threshold public good game with 
    n_players players and given threshold"""
    assert n_players >= 1
    assert 0 <= threshold <= n_players
    
    P = range(n_players)
    pls = players(*("i" + str(pos+1) for pos in P))
    global_actions("dont", "contribute")
    
    not_enough = Ou("not_enough", ac=False)
    enough = Ou("enough", ac=True)
    
    A = [dont, contribute]
    r = make_simultaneous_move ("", 
        players=pls,
        consequences={
        tuple(A[a[pos]] for pos in P): 
            OuN("", ou=enough if sum(a) >= threshold else not_enough)
        for a in itertools.product(*([0,1] for pos in P))
    })
    
    T = Tree("threshold_public_good_" + str(threshold) + "_of_" + str(n_players), ro=r)

    return T
