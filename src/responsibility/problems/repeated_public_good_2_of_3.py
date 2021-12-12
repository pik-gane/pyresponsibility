"""Three players simultaneously either contribute to a public good or don't.
They do this repeatedly for several rounds.
It is only acceptable if at least two contribute per round on average.""" 

n_rounds = 3

from ..__init__ import *

from itertools import product
from sympy import symbols
import numpy as np

global_players("i", "j", "k")

D = Action("D", desc="don't contribute")
C = Action("C", desc="contribute")
A = [D, C]

not_enough = Ou("not_enough", ac=False)
enough = Ou("enough", ac=True)

# compose per-round action combinations:
rcombs = list(product([0, 1], [0, 1], [0, 1]))

# create nodes from end to front:
nodes = {}

for r in range(n_rounds, -1, -1):
    # compose action combinations until round r:
    combs = product(*(rcombs for _ in range(r)))
    for c in combs:
        pre = "".join(str(x) for x in np.array(c).flatten())
        if r == n_rounds:
            # outcome node:
            nodes[c] = OuN("w"+pre, ou=enough if np.sum(c) >= 2 * n_rounds else not_enough)
        else:
            # simultaneous move decision nodes:
            nodes[c] = make_simultaneous_move ("v"+pre, players=(i, j, k), consequences={
                (A[ai], A[aj], A[ak]): nodes[c + ((ai, aj, ak),)]
                for ai in [0,1] for aj in [0,1] for ak in [0,1]
            })

T = Tree("repeated_public_good_2_of_3", ro=nodes[()])

T.make_globals()
