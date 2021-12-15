"""Backward Responsibility Functions from AAFRA.

Reference:
[AAFRA] Hiller, S., Israel, J., & Heitzig, J. (2021). An Axiomatic Approach to Formalized Responsibility Ascription.
"""

from ...functions import *

r_like = PRF(
    "r_like", 
    desc="Increase in guaranteed likelihood: by how much has the guaranteed likelihood (min over scen. and strat. of L) increased from this node to the next due to taking the given action?",
    function=(
        lambda T, G, v, a: 
            T.gamma(group=G, node=v.co[a]) 
            - T.gamma(group=G, node=v)
    ))

r_risk = PRF(
    "r_risk",
    desc="Worst-case shortfall in scenario-based minimization of likelihood: by how much has the scenario-specific minimally achievable likelihood increased from this node to the next due to taking the given action, in that scenario where this shortfall is largest? (max over scen. of min over strat. of L)",
    function=(
        lambda T, G, v, a:
            Max([T.Delta_omega(node=v, scenario=zeta, action=a)
                 for zeta in T.get_scenarios(node=v, group=G)])
    ))
    
r_negl = PRF(
    "r_negl",
    desc="Shortfall in minimizing worst-case likelihood: by how much has the risk increased from this node to the next due to taking the given action in comparison to the minimal value of this over all actions?",
    function=(
        lambda T, G, v, a:
            T.rho(group=G, node=v, action=a) - T.rho_min(group=G, node=v)
    ))

r_like_KSym = PRF(
    "r_like_KSym", 
    desc="Increase in guaranteed likelihood, maximized over possible current nodes: by how much might the guaranteed likelihood have increased from this node to the next due to taking the given action, given the uncertainty about the current node?",
    function=(
        lambda T, G, v, a: 
            Max([r_like(T, G, v2, a) for v2 in v.information_set.nodes])
    ))

