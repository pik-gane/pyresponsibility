# TODO: functions for normalizing trees by uniting nodes and exchanging the order of nodes

"""
Normalization rules:
====================

Draw a possibility node Y with k successors Z1...Zk towards the root:
---------------------------------------------------------------------
- PoN_X––Y ==> PoN_XY (cartesian product)
- PrN_X––Y ==> Y––PrN_X1...PrN_Xk (where PrN_Xj is PrN_X with Y replaced by Zj)
- DeN_X––Y ==> Y––DeN_X1...DeN_Xk (where DeN_Xj is DeN_X with Y replaced by Zj), information sets DeN_Xj.ins = DeN_X.ins 

Draw a decision node Y of player i with a singleton information set towards the root if possible:
-------------------------------------------------------------------------------------------------
- DeN_X(i,singleton ins)––Y ==> DeN_XY(i) (cartesian product)
- PrN_X––Y ==> see below!
- PoN_X––Y ==> similar to PrN_X––Y

Push a probability node X with k probabilities {Zj:pj} away from the root if possible:
--------------------------------------------------------------------------------------
- X––PrN_Y:p ==> PrN_XY with Zj:pj in PrN_Y replaced by {Zj:p*pj} in PrN_XY
- X––Z1=DeN_Y{a1:W1...al:Wl} ==> DeN_Y––X1...Xl (where Xi is X with Z1 replaced by Wi) 



"""