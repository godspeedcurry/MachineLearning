#it can generate a 8*8 matrix which is centrosymmetric 
"""
100 -10  11   6   6  11 -10 100
-10 -20   1   2   2   1 -20 -10
 11   1   5   4   4   5   1  11
  6   2   4   0   0   4   2   6
  6   2   4   0   0   4   2   6
 11   1   5   4   4   5   1  11
-10 -20   1   2   2   1 -20 -10
100 -10  11   6   6  11 -10 100
"""

import numpy as np
e = [[0 for i in range(8)] for j in range(8)]
e[0][0] = 100
e[0][1] = -10
e[0][2] = 11
e[0][3] = 6

e[1][1] = -20
e[1][2] = 1
e[1][3] = 2

e[2][2] = 5
e[2][3] = 4

e[3][3] = 2

for i in range(4):
	for j in range(i,4):
		e[i][7-j] = e[i][j] 

for i in range(8):
	for j in range(i,8):
		e[7-j][7-i] = e[i][j] 	

for i in range(8):
	for j in range(8):
		e[j][i] = e[i][j]

for i in range(8):
	for j in range(8):
		print ("{:3d}".format(e[i][j])),

	print('')
print (e)
