"""Three players simultaneously either contribute to a public good or don't.
It is only acceptable if at least two contribute.""" 

from ..__init__ import *

from sympy import symbols

global_players("i", "j", "k")
global_actions("dont", "contribute")

not_enough = Ou("not_enough", ac=False)
enough = Ou("enough", ac=True)

all_vks = []

vjs = [] 
for ai in [0,1]:
    vks = [] 
    for aj in [0, 1]:
        vk = DeN("", pl=k, co={
            dont: OuN("", ou=enough if ai + aj >= 2 else not_enough),
            contribute: OuN("", ou=enough if ai + aj + 1 >= 2 else not_enough)
        })
        vks.append(vk)        
    vj = DeN("", pl=j, co={
        dont: vks[0],
        contribute: vks[1] 
    })
    vjs.append(vj)
    all_vks += vks

vi = DeN("", pl=i, co={
    dont: vjs[0],
    contribute: vjs[1] 
})

InS("i_and_j_unobserved", no=set(all_vks))
InS("i_unobserved", no=set(vjs))

T = Tree("public_good_2_of_3", ro=vi)

T.make_globals()
