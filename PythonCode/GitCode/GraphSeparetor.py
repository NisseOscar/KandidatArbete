import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve

class GraphSeparetor:
    def __init__(self, data, n_neighbors):
        self.data = data

    #   Set all points that belong to the lower crurve to one
    def ConstructGraph(self, sepRight, sepLeft, incRight, incLeft, tol_merged):
        lowerCurve = np.zeros(len(self.data[:,1]))

        for i in range(0,len(sepRight)-1):
            # TODO tol!!
            indexPoints = np.where((self.data[:,1] <= sepRight[i,1]) & (self.data[:,1] >= sepRight[i+1,1]) & (self.data[:,0] > sepRight[i,0]-0.005) & (self.data[:,0] > sepRight[0,0]))
            if self.isMergedRight(incRight, sepRight, i, tol_merged):
                lowerCurve[indexPoints] = 1
            else:
                for point in indexPoints[0]:
                    if self.data[point,1] <=  sepRight[i,1] + incRight[i] * (self.data[point,0] - sepRight[i,0]):
                        lowerCurve[point] = 1

        for i in range(0,len(sepLeft)-1):
            indexPoints = np.where((self.data[:,1] <= sepLeft[i,1]) & (self.data[:,1] >= sepLeft[i+1,1]) & (self.data[:,0] < sepLeft[i,0]+0.005) & (self.data[:,0] < sepLeft[0,0]))
            if self.isMergedLeft(incLeft, sepLeft, i, tol_merged):
                lowerCurve[indexPoints] = 1
            else:
                for point in indexPoints[0]:
                    if self.data[point,1] <=  sepLeft[i,1] + incLeft[i] * (self.data[point,0] - sepLeft[i,0]):
                        lowerCurve[point] = 1

        return lowerCurve

        # Calculates distance from point to the closest point on the separator
    def distFromSep(self, inclination, separator, point, i):
        x = (point[1] + point[0]/inclination[i] - separator[i,1] + inclination[i]*separator[i,0])/(inclination[i] + 1/inclination[i])
        y =  separator[i,1] + inclination[i] * (x - separator[i,0])
        return np.sqrt((x - point[0])**2  + (y - point[1])**2)

        # Returns all inidices above the separator
    def pointsAboveSeparator(self, inclination, separator,i):
        return self.data[:,1] >=  inclination[i] * (self.data[:,0] - separator[i,0]) + separator[i,1]
        # Returns all inidices below the separator
    def pointsBelowSeparator(self, inclination, separator, i):
        return self.data[:,1] <=  inclination[i] * (self.data[:,0] - separator[i,0]) + separator[i,1]

    def isMergedRight(self, inclination, separator, i, tol_merged):
        top = np.where((self.data[:,0] > separator[i-1,0]) & (self.data[:,1] < separator[i-1,1]) & (self.data[:,1] > separator[i,1]) & self.pointsAboveSeparator(inclination, separator, i))
        bottom = np.where((self.data[:,0] > separator[i-1,0]) & (self.data[:,1] < separator[i-1,1]) & (self.data[:,1] > separator[i,1]) &  self.pointsBelowSeparator(inclination, separator, i))

        if np.size(top) < 1 or np.size(bottom) < 1:
            if np.size(top) > 1:
                bottom = top
            elif np.size(bottom) > 1:
                top = bottom
            else:
                return False

        topMean = [np.mean(self.data[top,0]), np.mean(self.data[top,1])]
        bottomMean = [np.mean(self.data[bottom,0]), np.mean(self.data[bottom,1])]

        return self.distFromSep(inclination, separator, topMean, i-1) < tol_merged and self.distFromSep(inclination, separator, bottomMean, i-1) < tol_merged

    def isMergedLeft(self, inclination, separator, i, tol_merged):

        top = np.where((self.data[:,0] < separator[i-1,0]) & (self.data[:,1] < separator[i-1,1]) & (self.data[:,1] > separator[i,1]) & self.pointsAboveSeparator(inclination, separator, i))
        bottom = np.where((self.data[:,0] < separator[i-1,0]) & (self.data[:,1] < separator[i-1,1]) & (self.data[:,1] > separator[i,1]) &  self.pointsBelowSeparator(inclination, separator, i))

        if np.size(top) < 1 or np.size(bottom) < 1:
            if np.size(top) > 1:
                bottom = top
            elif np.size(bottom) > 1:
                top = bottom
            else:
                return False

        topMean = [np.mean(self.data[top,0]), np.mean(self.data[top,1])]
        bottomMean = [np.mean(self.data[bottom,0]), np.mean(self.data[bottom,1])]

        return self.distFromSep(inclination, separator, topMean, i-1) < tol_merged and self.distFromSep(inclination, separator, bottomMean, i-1) < tol_merged

    def findSecondCurve(self, interval, tol_middlePoint):
        for i in range(1,len(interval)):
            # Find the points furthest to the right an left for each interval
            indexMax = int(np.argmax(np.where((self.data[:,1] > interval[i]) & (self.data[:,1] < interval[i-1]), self.data[:,0], -np.Inf)))
            indexMin = int(np.argmin(np.where((self.data[:,1] > interval[i]) & (self.data[:,1] < interval[i-1]), self.data[:,0], np.Inf)))
            right = self.data[indexMax,0]
            left = self.data[indexMin,0]
            dist = (right - left) /2
            middlePoints  = np.argmax(np.where((self.data[:,0]<left + dist + tol_middlePoint * dist) & (self.data[:,0] > left + dist - tol_middlePoint * dist) & (self.data[:,1] > interval[i]) & (self.data[:,1] < interval[i-1]), 1, 0))
            if middlePoints > 0:
                #plt.scatter(self.data[middlePoints,0], self.data[middlePoints,1], c ='r')
                return middlePoints, i

    def constructsepectories(self, tol_merged, tol_middlePoint, tol_int, nbr_int):

        # tol_merged: Tolerance for how close the graphs need to be to be inseparable
        # tol_middlePoint: Tolerance for how large intervals we look for the max value of the lower graph
        # tol_int: Tolerance for how large intervals we look for points when constructing the middle sepectory
        # tol_int: Number of intervals that the graphs are devided into

        indexMaxTopGraph = np.argmax(self.data[:,1])
        lowest = np.min(self.data[:,1])
        highest = np.max(self.data[:,1])
        interval = np.linspace(lowest, highest, nbr_int)[::-1]

        [startIndexLowerGraph, startInterval] = self.findSecondCurve(interval, tol_middlePoint)
        #print(self.data[startIndexLowerGraph,:])
        countRight = 1
        countLeft = 1

        # Discrete sepectories between the graphs
        sepRight = np.zeros((nbr_int-startInterval+1,2))
        sepLeft = np.zeros((nbr_int-startInterval+1,2))

        # The inclination in each interval
        incRight = np.zeros(nbr_int-startInterval)
        incLeft = np.zeros(nbr_int-startInterval)

        # Set a value between the max values of the two graphs as start values
        startPointX = self.data[startIndexLowerGraph,0] +  (self.data[indexMaxTopGraph,0] - self.data[startIndexLowerGraph,0]) / 7
        startPointY = self.data[startIndexLowerGraph,1] +  (self.data[indexMaxTopGraph,1] - self.data[startIndexLowerGraph,1]) / 7

        xPrevRight = startPointX
        xPrevLeft = startPointX

        sepRight[0,:] = [startPointX, startPointY]
        sepLeft[0,:] = [startPointX, startPointY]

        for i in range(startInterval, nbr_int-1):
            right = np.where((self.data[:,0]>xPrevRight) & (self.data[:,1] > interval[i] - tol_int) & (self.data[:,1] < interval[i] + tol_int))
            left = np.where((self.data[:,0]<xPrevLeft) & (self.data[:,1] > interval[i] - tol_int) & (self.data[:,1] < interval[i] + tol_int))

            if np.size(right) > 0:
                #print(right)
                right = right[0]
                indexTopRight = np.argmax(self.data[right,0])
                indexBottomRight = np.argmin(self.data[right,0])
                if indexTopRight != indexBottomRight:
                    sepRight[countRight,0] = (self.data[right[indexTopRight],0] +self.data[right[indexBottomRight],0])/2
                    sepRight[countRight,1] = (self.data[right[indexTopRight],1] + self.data[right[indexBottomRight],1])/2

                    incRight[countRight-1] = (sepRight[countRight,1] - sepRight[countRight -1,1]) / (sepRight[countRight ,0] - sepRight[countRight -1,0])
                    xPrevRight = self.data[right[indexBottomRight],0]
                    countRight = countRight + 1

            if  np.size(left) > 0:
                #print(left)
                #print(len(topLeft))
                left = left[0]
                indexTopLeft = np.argmax(self.data[left,0])
                indexBottomLeft = np.argmin(self.data[left,0])
                if indexTopRight != indexBottomRight:
                    sepLeft[countLeft,0] = (self.data[left[indexTopLeft],0] + self.data[left[indexBottomLeft],0])/2
                    sepLeft[countLeft,1] = (self.data[left[indexTopLeft],1] + self.data[left[indexBottomLeft],1])/2

                    incLeft[countLeft-1] = (sepLeft[countLeft,1] - sepLeft[countLeft-1,1]) / (sepLeft[countLeft,0] - sepLeft[countLeft-1,0])
                    xPrevLeft = self.data[left[indexTopLeft],0]
                    countLeft = countLeft + 1

        sepRight[countRight] = self.data[np.argmax(self.data[:,0])]
        sepLeft[countLeft] = self.data[np.argmin(self.data[:,0])]
        incRight[countRight-1] = (sepRight[countRight,1] - sepRight[countRight -1,1]) / (sepRight[countRight ,0] - sepRight[countRight -1,0])
        incLeft[countLeft-1] = (sepLeft[countLeft,1] - sepLeft[countLeft-1,1]) / (sepLeft[countLeft,0] - sepLeft[countLeft-1,0])


        return sepRight[:countRight+1], sepLeft[:countLeft+1], incRight[:countRight+1], incLeft[:countLeft+1]

    def SeperateGraphs(self, colPlot, tol_merged, tol_middlePoint, tol_int, nbr_int):
        [sepRight, sepLeft, incRight, incLeft] = self.constructsepectories(tol_merged, tol_middlePoint, tol_int, nbr_int)

        # # 1 if data point j belongs to graph i, zero otherwise. i in nbr graphs, j in nbr datapoints
        graphMatrix = np.zeros((2,len(self.data)))

        # Construct lower graph
        lowerGraph = self.ConstructGraph(sepRight, sepLeft, incRight, incLeft, tol_merged)
        symbols = np.where(lowerGraph>0,"u","l")

        if colPlot:
            col = np.where(symbols == 'u','r','g')
            plt.scatter(self.data[:,0],self.data[:,1],c=col, s=2)
            #plt.plot(sepRight[:,0], sepRight[:,1], 'black')
            #plt.plot(sepLeft[:,0], sepLeft[:,1], 'black')
            plt.show()
        return symbols
