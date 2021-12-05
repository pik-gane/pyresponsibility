from time import time

from responsibility import *
#from responsibility.problems.qrpc_fig3 import T
#from responsibility.problems.drsc_fig1a import T
#from responsibility.problems.drsc_fig1b import T
#from responsibility.problems.drsc_fig2b import T
from responsibility.problems.repeated_public_good_2_of_3 import *

print(len(T.nodes))

#print(repr(T))

#T.draw("/tmp/test.pdf", show=True)

sc_allD = Scenario("allD", anchor=vi, tr={
    S: D for S in T.information_sets.values() if S.player != i
})
sc_jCkD = Scenario("jCkD", anchor=vi, tr={
    S: (C if S.player == j else D) for S in T.information_sets.values() if S.player != i
})
st_iC = Strategy("iC", anchor=vi, ch={
    S: C for S in T.get_information_sets(i).values()
})

start = time()
dist = T.get_outcome_distribution(sc_jCkD, st_iC)
print(dist)
print(time()-start, "sec.")

start = time()
print(len(list(T.get_scenarios(vi, player=i))))
print(np.mean([T.get_outcome_distribution(sc, st_iC).get(enough, 0) for sc in T.get_scenarios(vi, player=i)]))
print(time()-start, "sec.")

start = time()
print(sum(1 for _ in T.get_strategies(vi, player=i)))
print(np.mean([T.get_outcome_distribution(scenario=sc_jCkD, strategy=st).get(enough, 0) for st in T.get_strategies(vi, player=i)]))
print(time()-start, "sec.")



exit()

T.make_globals()

print()

print(T.nodes)
print(T.players)
print(T.outcomes)
print(T.actions)
print(T.inner_nodes)
print(T.leaf_nodes)
print(T.possibility_nodes)
print(T.probability_nodes)
print(T.decision_nodes)
print(T.information_sets)

#print(v4_unknown_warming.information_set.nodes)
#print(w14_cooling_knowingly_prevented.history)


