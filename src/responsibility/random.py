from numpy.random import choice, uniform
import sympy as sp

# TODO: when putting two DeN into an InS, immediately bring them together as successors of the next node.

from .players import *
from .outcomes import *
from .actions import *
from .nodes import *
from .trees import Tree

def random_tree (n_players, n_leafs, 
                 p_PoN=0.35, p_PrN=0.35, p_DeN=0.3,
                 p4=0.5,
                 symbolic=False):
    """Returns a random Tree with n_players many players and n_leafs many leafs"""
    assert n_players >= 0
    assert n_leafs >= 1
    
    pls = players(*("i" + str(k+1) for k in range(n_players)))
    
    global n_nodes, n_Ou
    n_InS = n_Ou = 0

    def make_ou():
        global n_Ou
        n_Ou = n_Ou + 1
        return Ou("o" + str(n_Ou), is_acceptable = choice([False, True]))
        
    roots = [OuN("w" + str(k+1), ou=make_ou()) 
             for k in range(n_leafs)]
    n_nodes = n_leafs
    
    a, b = actions("a", "b")
    
    while len(roots) > 1:
        ty = choice([PoN, PrN, DeN], p=[p_PoN, p_PrN, p_DeN])
        if uniform() < p4 and len(roots) >= 4:
            # add two indistinguishable decision nodes for the same player
            su11, su12, su21, su22 = choice(roots, size=4, replace=False)
            i = choice(pls)
            # put both in the same information set:
            n_InS += 1
            ins = InS("S" + str(n_InS))
            n_nodes += 1
            su1 = DeN("v" + str(n_nodes), pl=i, ins=ins, co={a: su11, b: su12})
            n_nodes += 1
            su2 = DeN("v" + str(n_nodes), pl=i, ins=ins, co={a: su21, b: su22})
            roots.append(su1)
            roots.append(su2)
            roots.remove(su11)
            roots.remove(su12)
            roots.remove(su21)
            roots.remove(su22)
            forbidden_player = i
        else:
            su1, su2 = choice(roots, size=2, replace=False)
            forbidden_player = None
        if ty == PoN:
            n_nodes += 1
            roots.append(PoN("v" + str(n_nodes), su={su1, su2}))
        elif ty == PrN:
            n_nodes += 1
            p = sp.symbol("p" + str(n_nodes)) if symbolic else choice(np.arange(1, 100) / 100)
            roots.append(PrN("", pr={su1: p, su2: 1 - p}))
        else:
            i = choice(pls)
            while i == forbidden_player:
                i = choice(pls)
            n_nodes += 1
            roots.append(DeN("v" + str(n_nodes), pl=i, co={a: su1, b: su2}))
        roots.remove(su1)
        roots.remove(su2)

    return Tree("random_tree", ro=roots.pop(), total_recall=True)