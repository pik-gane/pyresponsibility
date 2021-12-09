from numpy.random import choice, uniform
import sympy as sp

from .players import *
from .outcomes import *
from .actions import *
from .nodes import *
from .trees import Tree

def random_tree (n_players, n_leafs, p_PoN=0.35, p_PrN=0.35, p_1DeN=0.2, p_2DeN=0.1,
                 symbolic=False, total_recall=False):
    """Returns a random Tree with n_players many players and approximately 
    n_leafs many leafs"""
    assert n_players >= 0
    assert n_leafs >= 1
    
    pls = players(*("i" + str(k+1) for k in range(n_players)))
    
    roots = [OuN("w" + str(k+1), 
                 ou=Ou("o" + str(k+1), is_acceptable = choice([False, True]))) 
             for k in range(n_leafs)]
    
    a, b = actions("a", "b")
    
    n_PrN = n_InS = 0
    
    while len(roots) > 1:
        ty = choice([PoN, PrN, DeN, (DeN, DeN)], p=[p_PoN, p_PrN, p_1DeN, p_2DeN])
        if ty == (DeN, DeN):
            # add two indistinguishable decision nodes for the same player
            if len(roots) < 4:
                continue
            su11, su12, su21, su22 = choice(roots, size=4, replace=False)
            roots.remove(su11)
            roots.remove(su12)
            roots.remove(su21)
            roots.remove(su22)
            i = choice(pls)
            if total_recall:
                assert 0==1
                # TODO: make consistent
            # put both in the same information set:
            n_InS += 1
            ins = InS("S" + str(n_InS))
            roots.append(DeN("", pl=i, ins=ins, co={a: su11, b: su12}))
            roots.append(DeN("", pl=i, ins=ins, co={a: su21, b: su22}))
        else:
            su1, su2 = choice(roots, size=2, replace=False)
            roots.remove(su1)
            roots.remove(su2)
            if ty == PoN:
                v = PoN("", su={su1, su2})
            elif ty == PrN:
                n_PrN += 1
                p = sp.symbol("p" + str(n_PrN)) if symbolic else choice(np.linspace(.01,0.99,99))
                v = PrN("", pr={su1: p, su2: 1 - p}) 
            else:
                i = choice(pls)
                if total_recall:
                    assert 0==1
                    # TODO: make consistent
                v = DeN("", pl=i, co={a: su1, b: su2})
            roots.append(v)
            
    return Tree("random_tree", ro=roots.pop())
    
    