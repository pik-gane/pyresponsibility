"""Three named_players simultaneously either contribute to a public good or don't.
It is only acceptable if at least two contribute.""" 

from ..__init__ import *

from sympy import symbols

global_players("i", "j", "k")
global_actions("dont", "contribute")

not_enough = Ou("not_enough", ac=False)
enough = Ou("enough", ac=True)

A = [dont, contribute]
r = make_simultaneous_move ("v1", players=(i, j, k), consequences={
    (A[ai], A[aj], A[ak]): 
        OuN("w"+str(ai)+str(aj)+str(ak), ou=enough if ai + aj + ak >= 2 else not_enough)
    for ai in [0,1] for aj in [0,1] for ak in [0,1]
})

T = Tree("public_good_2_of_3", ro=r)

T.make_globals()
