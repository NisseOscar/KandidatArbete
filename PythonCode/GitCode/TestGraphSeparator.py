from GraphSeparetor import *
import numpy as np
#
data = np.loadtxt('Fitz4DManifold.txt')


#data[:,1] = 5 *data[:,1]
data = np.transpose(np.array([data[:-1,0], data[1:,0]]))

nb = GraphSeparetor(data, 40)
#nb.constructTrajectories()
nb.SeperateGraphs(True, 0.006, 0.1, 0.0005, 70,  0.005)
#nb.constructTrajectories()
#symbols = nb.SeperateGraphs(colPlot = True)
#print(symbols)
# A = np.array([[1, 1, 0], [1, 1, 1]])
# print(A)
# print(np.where((A[0,:] == 1) &(A[1,:] == 1), A[1,:], -1))
