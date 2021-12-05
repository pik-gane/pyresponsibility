from responsibility import *
from responsibility.problems.qrpc_fig3 import T
#from responsibility.problems.drsc_fig1a import T
#from responsibility.problems.drsc_fig1b import T
#from responsibility.problems.drsc_fig2b import T

print(repr(T))

T.draw("/tmp/test.pdf", show=True)

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
#print(T.get_decision_nodes(i))
#print(T.get_information_sets(i))

#print(v4_unknown_warming.information_set.nodes)
#print(w14_cooling_knowingly_prevented.history)



sc = Scenario("upper", anchor=r, tr={v1: w1})
st = Strategy("b", anchor=r, ch={r.information_set: b})

dist = T.get_outcome_distribution(sc, st)
print(dist)

