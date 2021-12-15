"""Backward Responsibility Functions based on the idea of cooperation.
"""

from ...functions import *

r_coop = PRF(
    "r_coop",
    desc="Worst-case increase in cooperatively achievable likelihood",
    function=(
        lambda T, unused_G, v, a:
            Max([
                T.cooperatively_achievable_likelihood(
                    node=v, env_scenario=eps,
                    fixed_choices={v.information_set: a}) 
                - T.cooperatively_achievable_likelihood(
                    node=v, env_scenario=eps)
                for eps in T.get_scenarios(node=v, group=T.players)
            ])
    ))
