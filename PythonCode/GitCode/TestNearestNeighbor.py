from NearestNeighbor import *
import numpy as np

data = np.loadtxt('Fitz4DManifold.txt')
data = np.transpose(np.array([data[:-1,0], data[1:,0]]))

nb = NearestNeighbor(data, 15)
symbols = nb.SeperateGraphs(colPlot = True)
#print(symbols)
