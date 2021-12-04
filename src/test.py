from responsibility import *
from responsibility.problems.qrpc_fig3 import *

print(tree.nodes)
print(tree.players)
print(tree.outcomes)
print(tree.actions)
print(tree.inner_nodes)
print(tree.leaf_nodes)
print(tree.possibility_nodes)
print(tree.probability_nodes)
print(tree.decision_nodes)
print(tree.get_decision_nodes(i))
print(tree.get_information_sets(i))

print(w1.history)

sc = Scenario("upper", anchor=r, tr={v1: w1})
st = Strategy("b", anchor=r, ch={r.information_set: b})

dist = tree.get_outcome_distribution(sc, st)
print(dist)

