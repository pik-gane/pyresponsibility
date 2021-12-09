from .players import *
from .outcomes import *
from .actions import *
from .nodes import *
from .trees import Tree
from np.random import choice

def random_tree (n_players, n_leafs, p_PoN=0.35, p_PrN=0.35, p_1DeN=0.2, p_2DeN=0.1):
    """Returns a random Tree with n_players many players and approximately 
    n_leafs many leafs"""
    assert n_players >= 0
    assert n_leafs >= 1
    
    pls = players(*("i" + str(k+1) for k in range(n_players)))
    
    roots = {OuN("w" + str(k+1), 
                 ou=Ou("o" + str(k+1), is_acceptable = choice([False, True]))) 
             for k in range(n_leafs)}
    
    a, b = actions("a", "b")
    
    while len(roots) > 1:
        ty = choice([PoN, PrN, DeN, (DeN, DeN)], p=[p_PoN, p_PrN, p_1DeN, p_2DeN])
        if ty == (DeN, DeN):
            pass
        else:
            su1, su2 = choice(roots, size=2, replace=False)
            roots.remove(su1)
            roots.remove(su2)
            roots.add(
                PoN())
        
    return roots.pop().tree