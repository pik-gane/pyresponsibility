from numpy.random import choice, uniform
import sympy as sp

# TODO: when putting two DeN into an InS, immediately bring them together as successors of the next node.

from .players import *
from .outcomes import *
from .actions import *
from .nodes import *
from .trees import Tree

def random_tree (n_players, n_leafs, 
                 p_PoN=0.3, p_PrN=0.3, p_1DeN=0.25, p_2DeN=0.15,
#                 p_PoN=0.0, p_PrN=0.0, p_1DeN=0.0, p_2DeN=1.0,
                 symbolic=False, total_recall=False):
    """Returns a random Tree with n_players many players and approximately 
    n_leafs many leafs"""
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
    
    def make_other(i, su1, su2):
        global n_nodes
        roots1 = set([su1])
        roots2 = set([su2])
        # find the roots of all indistinguishable nodes of all DeNs on su1 and su2's branches:
        lens1 = set()
        lens2 = set()
        for x in su1.branch.get_decision_nodes(i):
            for y in x.information_set.nodes:
                roots1.add(y.path[0])
                lens1.add(len(y.choice_history))
        for x in su2.branch.get_decision_nodes(i):
            for y in x.information_set.nodes:
                roots2.add(y.path[0])
                lens2.add(len(y.choice_history))
        if not (roots1.isdisjoint(roots2) 
                and roots1.issubset(roots) and roots2.issubset(roots)
                and len(lens1) < 2 and len(lens2) < 2):
            return "incompatible"
        roots1.remove(su1)
        roots2.remove(su2)
        for s in list(roots1) + list(roots2):
            roots.remove(s)
        if len(roots1) > 0 and len(roots2) > 0:
            n_nodes += 1
            return DeN("v'" + str(n_nodes), pl=i, co={
                a: PoN("va" + str(n_nodes), su=roots1) if len(roots1) > 1 else roots1.pop(),
                b: PoN("vb" + str(n_nodes), su=roots2) if len(roots2) > 1 else roots2.pop()
            })
        elif len(roots1) > 0:
            n_nodes += 1
            return DeN("v'" + str(n_nodes), pl=i, co={
                a: PoN("va" + str(n_nodes), su=roots1) if len(roots1) > 1 else roots1.pop(),
                b: OuN("vb" + str(n_nodes), ou=make_ou())
            })    
        elif len(roots2) > 0:
            n_nodes += 1
            return DeN("v'" + str(n_nodes), pl=i, co={
                a: OuN("va" + str(n_nodes), ou=make_ou()),
                b: PoN("vb" + str(n_nodes), su=roots2) if len(roots2) > 1 else roots2.pop()
            })
        return None
        
    while len(roots) > 1:
        ty = choice([PoN, PrN, DeN, (DeN, DeN)], p=[p_PoN, p_PrN, p_1DeN, p_2DeN])
        if ty == (DeN, DeN):
            # add two indistinguishable decision nodes for the same player
            if len(roots) < 4:
                continue
            su11, su12, su21, su22 = choice(roots, size=4, replace=False)
            i = choice(pls)
            if total_recall:
                other1 = make_other(i, su11, su12)
                if other1 == "incompatible": 
                    continue
                other2 = make_other(i, su21, su22)
            else:
                other1 = other2 = None
            # put all in the same information set:
            n_InS += 1
            ins = InS("S" + str(n_InS))
            n_nodes += 1
            roots.append(DeN("v" + str(n_nodes), pl=i, ins=ins, co={a: su11, b: su12}))
            if other1 is not None:
                roots.append(other1)
                other1._i_information_set = None
                ins.add_node(other1)
            roots.remove(su11)
            roots.remove(su12)
            if other2 != "incompatible":
                n_nodes += 1
                roots.append(DeN("v" + str(n_nodes), pl=i, ins=ins, co={a: su21, b: su22}))
                if other2 is not None:
                    roots.append(other2)
                    other2._i_information_set = None
                    ins.add_node(other2)
                roots.remove(su21)
                roots.remove(su22)
        else:
            su1, su2 = choice(roots, size=2, replace=False)
            if ty == PoN:
                n_nodes += 1
                roots.append(PoN("v" + str(n_nodes), su={su1, su2}))
            elif ty == PrN:
                n_nodes += 1
                p = sp.symbol("p" + str(n_nodes)) if symbolic else choice(np.arange(1, 100) / 100)
                roots.append(PrN("", pr={su1: p, su2: 1 - p}))
            else:
                i = choice(pls)
                if total_recall:
                    other = make_other(i, su1, su2)
                    if other == "incompatible": 
                        continue
                else:
                    other = None
                n_nodes += 1
                v = DeN("v" + str(n_nodes), pl=i, co={a: su1, b: su2})
                roots.append(v)
                if other is not None:
                    roots.append(other)
                    n_InS += 1
                    InS("S" + str(n_InS), nodes={v, other})
            roots.remove(su1)
            roots.remove(su2)

    return Tree("random_tree", ro=roots.pop(), total_recall=total_recall)
    
    