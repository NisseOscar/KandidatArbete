from GraphSeparetor import *
import numpy as np
#
data = np.loadtxt('data2.txt')


#data[:,1] = 5 *data[:,1]
data = np.transpose(np.array([data[:-1], data[1:]]))

nb = GraphSeparetor(data, 40)
#nb.constructTrajectories()
nb.SeperateGraphs(True, 0.00018, 0.1, 0.0005, 60)
#nb.constructTrajectories()
#symbols = nb.SeperateGraphs(colPlot = True)
#print(symbols)
# A = np.array([[1, 1, 0], [1, 1, 1]])
# print(A)
# print(np.where((A[0,:] == 1) &(A[1,:] == 1), A[1,:], -1))
