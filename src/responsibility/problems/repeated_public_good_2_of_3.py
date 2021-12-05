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
            # decision nodes:

            all_vks = []
            
            vjs = [] 
            for ai in [0, 1]:
                vks = [] 
                for aj in [0, 1]:
                    vk = DeN("v"+pre+str(ai)+str(aj)+"k", pl=k, co={
                        D: nodes[c + ((ai, aj, 0),)],
                        C: nodes[c + ((ai, aj, 1),)] 
                    })
                    vks.append(vk)        
                vj = DeN("v"+pre+str(ai)+"j", pl=j, co={
                    D: vks[0],
                    C: vks[1]
                })
                vjs.append(vj)
                all_vks += vks
            
            nodes[c] = DeN("v"+pre+"i", pl=i, co={
                D: vjs[0],
                C: vjs[1]
            })
            
            InS("s"+pre+"k", no=set(all_vks))
            InS("s"+pre+"j", no=set(vjs))

T = Tree("repeated_public_good_2_of_3", ro=nodes[()])

T.make_globals()
