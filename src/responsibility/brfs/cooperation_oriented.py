"""Backward Responsibility Functions based on the idea of cooperation.
"""

from ..functions import *

r_coop = PRF(
    "r_coop",
    desc="Increase in cooperatively achievable worst-case likelihood",
    function=(
        lambda T, unused_G, v, a:
            T.cooperatively_achievable_worst_case_likelihood(node=v, 
                 fixed_choices={v.information_set: a}) 
            - T.cooperatively_achievable_worst_case_likelihood(node=v)
    ))
