import numpy as np
import matplotlib.pyplot as plt
#x = np.array([-2, 1, 0, -1, 2, -3])
#y = np.array([4, 1, 20, 1, 4, 9])

class SymbolicDynamics:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #symbolicRepresentation(x, y)
        #plot(x, y)
    def FindExtremePoint(x, y):
        yMax = np.max(y)
        yIndMax = np.argmax(y)
        yMin = np.min(y)
        yIndMin = np.argmin(y)
        xMid = np.median(x)
        if np.abs(xMid-x[yIndMax]) < np.abs(xMid-x[yIndMin]):
            index = yIndMax
        else:
            index = yIndMin
        # yExtreme = np.max(y)
        # index = np.argmax(y)
        # if x[index] == np.max(x) or x[index] == np.min(x):
        #     yExtreme = np.min(y)
        #     index = np.argmin(y)
        return index

    def symbolicRepresentation(x, y):
        index = SymbolicDynamics.FindExtremePoint(x, y)
        z = [0 if  i <= x[index] else 1 for i in x]
        return np.array(z)

    def colorPlot(x, y, z):
        # index = SymbolicDynamicsRossler.FindExtremePoint(x, y)
        fig = plt.figure()
        # ax = fig.add_subplot(211)
        # ax.scatter(x,y,s=1)
        # ax = fig.add_subplot(212)
        #col = np.where(x<x[index],'k',np.where(y<5,'b','r'))
        col =  np.where(z < 1, 'y', 'b')
        #col = np.where(x == x[index], 'k', np.where(x < x[index], 'r', 'b'))
        #, np.where(x < x[index],'r'), np.where(x < x[index],'b')
        plt.scatter(x, y, c=col, s=5, linewidth=0)
        plt.show()
