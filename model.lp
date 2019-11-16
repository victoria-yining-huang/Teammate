\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  10000 var(4) + 10000 var(5) + var(8) + var(9) + var(10) + var(11)
   + 100 var(12) + var(15) + 10 var(16) + 10 var(17)
Subject To
 constr(0): var(0) + var(1) = 1
 constr(1): var(2) + var(3) = 1
 constr(2): var(0) + var(2) + var(6) = 1
 constr(3): var(1) + var(3) + var(7) = 1
 constr(4): var(0) + var(2) - var(4) <= 1
 constr(5): var(1) + var(3) - var(5) <= 1
 constr(6): var(0) + var(2) + var(6) = 1
 constr(7): var(1) + var(3) + var(7) = 1
 constr(8): 5 var(0) - 6 var(2) + var(8) - var(10) = -0
 constr(9): 5 var(1) - 6 var(3) + var(9) - var(11) = -0
 constr(10): 5 var(0) + 6 var(2) - var(13) = -0
 constr(11): 5 var(1) + 6 var(3) - var(14) = -0
 constr(12): - var(13) + var(15) >= -0
 constr(13): - var(14) + var(15) >= -0
 constr(14): - var(6) + var(12) >= -0
 constr(15): - var(7) + var(12) >= -0
 constr(16): - 100 var(16) <= -1
 constr(17): - 100 var(17) <= -1
Bounds
Binaries
 var(0) var(1) var(2) var(3) var(4) var(5) var(16) var(17)
Generals
 var(6) var(7) var(8) var(9) var(10) var(11) var(12) var(13) var(14)
 var(15)
End
