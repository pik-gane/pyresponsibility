from responsibility import *
from responsibility.problems.qrpc_fig3 import T

print(repr(T))

T.make_globals()

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
print(T.get_decision_nodes(i))
print(T.get_information_sets(i))

print(w1.history)

sc = Scenario("upper", anchor=r, tr={v1: w1})
st = Strategy("b", anchor=r, ch={r.information_set: b})

dist = T.get_outcome_distribution(sc, st)
print(dist)

