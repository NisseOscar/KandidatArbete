import matplotlib.pyplot as plt
import numpy as np
from queue import Queue

class GraphSeparetor:
    def __init__(self, data, n_neighbors):
        self.data = data

    # tol_Graph: Removes points whichs x value is at least tol_Graph from its closest trajectory
    def ConstructGraph(self, trajRight, trajLeft, kRight, kLeft, mergedGraphsRight, mergedGraphsLeft, tol_Graph, topGraph):
        leftBranch = np.zeros(len(self.data[:,1]))
        rightBranch = np.zeros(len(self.data[:,1]))

        for i in range(len(trajRight)-1):
            for j in range(len(self.data[:,0])):
                if topGraph:
                    # Add to the right branch if the point is above right trajectory or
                    #if  ((self.data[j,1] < trajRight[i,1]) & (self.data[j,1] > trajRight[i+1,1]) & (self.data[j,0] > 0)) & (self.data[j,1] >  kRight[i] * (self.data[j,0] - trajRight[i,0]) + trajRight[i,1] or mergedGraphsRight[i]) or (self.data[j,1] > trajRight[0,1]):
                    if  ((self.data[j,1] < trajRight[i,1]) & (self.data[j,1] > trajRight[i+1,1]) & (self.data[j,0] > 0)) & (((self.data[j,1] >  kRight[i] * (self.data[j,0] - trajRight[i,0]) + trajRight[i,1]) & (self.data[j,0] > trajRight[i,0])) or mergedGraphsRight[i]):
                        rightBranch[j] = 1

                    # Add to the left branch if the point is above left trajectory
                    if  (self.data[j,1] < trajLeft[i,1]) & (self.data[j,1] > trajLeft[i+1,1]) & (self.data[j,0] < 0) & ((self.data[j,1] >  kLeft[i] * (self.data[j,0] - trajLeft[i,0]) + trajLeft[i,1]) or mergedGraphsLeft[i]) or (self.data[j,1] > trajRight[0,1]):
                        leftBranch[j] = 1
                else:
                    # Add to the right branch if the point is above rigt trajectory
                    if  ((self.data[j,1] < trajRight[i,1]) & (self.data[j,1] > trajRight[i+1,1]) & (self.data[j,0] > 0)) & ((self.data[j,1] <  kRight[i] * (self.data[j,0] - trajRight[i,0]) + trajRight[i,1] or mergedGraphsRight[i])):
                        rightBranch[j] = 1

                    # Add to the left branch if the point is above left trajectory
                    if  (self.data[j,1] < trajLeft[i,1]) & (self.data[j,1] > trajLeft[i+1,1]) & (self.data[j,0] < 0) & ((self.data[j,1] <  kLeft[i] * (self.data[j,0] - trajLeft[i,0]) + trajLeft[i,1]) or mergedGraphsLeft[i]):
                        leftBranch[j] = 1
                closestTrajRight = np.argmin(np.abs(trajRight[:,1] - self.data[j,1]))
                closestTrajLeft = np.argmin(np.abs(trajLeft[:,1] - self.data[j,1]))
                if (np.abs(self.data[j,0] - trajRight[closestTrajRight,0]) > tol_Graph and np.abs(self.data[j,0] - trajLeft[closestTrajLeft,0]) > tol_Graph):
                    rightBranch[j] = 0
                    leftBranch[j] = 0

        return np.where(rightBranch + leftBranch > 0, 1, 0)
    def constructTrajectories(self, tol_merged, tol_middlePoint, tol_int, nbr_int):
        # tol_merged: Tolerance for how close the graphs need to be to be inseparable
        # tol_middlePoint: Tolerance for how large intervals we look for the max value of the lower graph
        # tol_int: Tolerance for how large intervals we look for points when constructing the middle trajectory
        # tol_int: Number of intervals that the graphs are devided into
        indexMaxTopGraph = np.argmax(self.data[:,1])
        lowest = np.min(self.data[:,1])
        highest = np.max(self.data[:,1])
        interval = np.linspace(lowest, highest, nbr_int)[::-1]
        secondCurveFound = False

        # Discrete trajectories between the graphs
        trajRight = np.zeros((nbr_int,2))
        trajLeft = np.zeros((nbr_int,2))

        # The inclination in each interval
        kRight = np.zeros(nbr_int)
        kLeft = np.zeros(nbr_int)

        # True if the graphs in the interval are inseparable
        mergedGraphsRight = [False] * nbr_int
        mergedGraphsLeft = [False] * nbr_int

        start = -1
        middlePoint = 0

        for i in range(nbr_int):
            # Find the points furthest to the right an dleft for each interval
            indexMax = int(np.argmax(np.where((self.data[:,1] > interval[i] - tol_int) & (self.data[:,1] < interval[i] + tol_int), self.data[:,0], -np.Inf)))
            indexMin = int(np.argmin(np.where((self.data[:,1] > interval[i] - tol_int) & (self.data[:,1] < interval[i] + tol_int), self.data[:,0], np.Inf)))

            if (not secondCurveFound):
                start = start + 1
                right = self.data[indexMax,0]
                left = self.data[indexMin,0]
                dist = (right - left) /2
                middlePoints  = np.where((self.data[:,0]<left + dist + tol_middlePoint * dist) & (self.data[:,0] > left + dist - tol_middlePoint * dist) & (self.data[:,1] > interval[i] - tol_int) & (self.data[:,1] < interval[i] + tol_int), 1, 0)
                if (np.sum(middlePoints) > 1):
                    secondCurveFound = True
                    middlePoint = np.argmax(middlePoints)
                    xPrevRight = self.data[middlePoint,0]
                    xPrevLeft = self.data[middlePoint,0]

                    # Set a value between the max values of the two graphs as start values
                    startPointX = self.data[middlePoint,0] +  (self.data[np.argmax(self.data[:,1]),0] - self.data[middlePoint,0]) / 5
                    startPointY = self.data[middlePoint,1] +  (np.max(self.data[:,1]) - self.data[middlePoint,1]) / 5

                    trajRight[i,0] = startPointX
                    trajRight[i,1] = startPointY
                    trajLeft[i,0] = startPointX
                    trajLeft[i,1] = startPointY

            else:
                indexTopRight = int(np.argmax(np.where((self.data[:,0]>xPrevRight) & (self.data[:,1] > interval[i] - tol_int) & (self.data[:,1] < interval[i] + tol_int), self.data[:,0], np.NINF)))
                indexTopLeft = int(np.argmax(np.where((self.data[:,0]<xPrevLeft) & (self.data[:,1] > interval[i] - tol_int) & (self.data[:,1] < interval[i] + tol_int), self.data[:,0], np.NINF)))
                indexBottomRight = int(np.argmin(np.where((self.data[:,0]>xPrevRight) & (self.data[:,1] > interval[i] - tol_int) & (self.data[:,1] < interval[i] + tol_int), self.data[:,0], np.Inf)))
                indexBottomLeft = int(np.argmin(np.where((self.data[:,0]<xPrevLeft) & (self.data[:,1] > interval[i] - tol_int) & (self.data[:,1] < interval[i] + tol_int), self.data[:,0], np.Inf)))
                xPrevRight = self.data[indexBottomRight,0]
                xPrevLeft = self.data[indexTopLeft,0]
                trajRight[i,0] = (self.data[indexTopRight,0] + self.data[indexBottomRight,0])/2
                trajRight[i,1] = (self.data[indexTopRight,1] + self.data[indexBottomRight,1])/2
                trajLeft[i,0] = (self.data[indexTopLeft,0] + self.data[indexBottomLeft,0])/2
                trajLeft[i,1] = (self.data[indexTopLeft,1] + self.data[indexBottomLeft,1])/2


                indexTopRightDown = int(np.argmin(np.where((self.data[:,0]>xPrevRight) & (self.data[:,1] > interval[i] - tol_int) & (self.data[:,1] < interval[i] + tol_int) & (self.data[:,1] > kRight[i] * (self.data[:,0] - trajRight[i,0]) + trajRight[i,1]), self.data[:,0], np.Inf)))
                indexTopLeftDown = int(np.argmin(np.where((self.data[:,0]<xPrevLeft) & (self.data[:,1] > interval[i] - tol_int) & (self.data[:,1] < interval[i] + tol_int) & (self.data[:,1] > kLeft[i] * (self.data[:,0] - trajLeft[i,0]) + trajLeft[i,1]), self.data[:,0], np.Inf)))
                indexBottomRightUp = int(np.argmax(np.where((self.data[:,0]>xPrevRight) & (self.data[:,1] > interval[i] - tol_int) & (self.data[:,1] < interval[i] + tol_int) & (self.data[:,1] < kRight[i] * (self.data[:,0] - trajRight[i,0]) + trajRight[i,1]), self.data[:,0], np.NINF)))
                indexBottomLeftUp = int(np.argmax(np.where((self.data[:,0]<xPrevLeft) & (self.data[:,1] > interval[i] - tol_int) & (self.data[:,1] < interval[i] + tol_int) & (self.data[:,1] < kLeft[i] * (self.data[:,0] - trajLeft[i,0]) + trajLeft[i,1]), self.data[:,0], np.NINF)))

                # Distances to right branch
                distTopGraphToTrajRight = np.sqrt((self.data[indexTopRightDown,1] - trajRight[i,1])**2 + (self.data[indexTopRightDown,0]**2 - trajRight[i,0])**2)
                distBottomGraphToTrajRight = np.sqrt((trajRight[i,1] - self.data[indexBottomRightUp,1])**2 + (trajRight[i,0] - self.data[indexBottomRightUp,0])**2)

                # Distances to left branch
                distTopGraphToTrajLeft = np.sqrt((self.data[indexTopLeftDown,1] - trajLeft[i,1])**2 + (self.data[indexTopLeftDown,0]**2 - trajLeft[i,0])**2)
                distBottomGraphToTrajLeft = np.sqrt((trajLeft[i,1] - self.data[indexBottomLeftUp,1])**2 + (trajLeft[i,0] - self.data[indexBottomLeftUp,0])**2)

                # Set Merged to true if the graphs are close to the ttrajectory
                mergedGraphsRight[i] =  distTopGraphToTrajRight > tol_merged or distBottomGraphToTrajRight > tol_merged
                mergedGraphsLeft[i] =  distTopGraphToTrajLeft > tol_merged or distBottomGraphToTrajLeft > tol_merged

                kRight[i-1] = (trajRight[i,1] - trajRight[i-1,1]) / (trajRight[i,0] - trajRight[i-1,0])
                kLeft[i-1] = (trajLeft[i,1] - trajLeft[i-1,1]) / (trajLeft[i,0] - trajLeft[i-1,0])

        return trajRight[start:], trajLeft[start:], kRight[start:], kLeft[start:], mergedGraphsRight[start:], mergedGraphsLeft[start:]

    def SeperateGraphs(self, colPlot, tol_merged, tol_middlePoint, tol_int, nbr_int, tol_Graph):
        [trajRight, trajLeft, kRight, kLeft, mergedGraphsRight, mergedGraphsLeft] = self.constructTrajectories(tol_merged, tol_middlePoint, tol_int, nbr_int)

        # 1 if data point j belongs to graph i, zero otherwise. i in nbr graphs, j in nbr datapoints
        graphMatrix = np.zeros((2,len(self.data)))

        # Construct Upper graph
        graphMatrix[0,:] = self.ConstructGraph(trajRight, trajLeft, kRight, kLeft, mergedGraphsRight, mergedGraphsLeft, tol_Graph, True)

        # Construct lower graph
        graphMatrix[1,:]  = self.ConstructGraph(trajRight, trajLeft, kRight, kLeft, mergedGraphsRight, mergedGraphsLeft, tol_Graph, False)
        # Gives each data point a different symbol depending on if it belongs to the Upper graph, lower graph, both graphs or non of the graphs
        # b = both graphs, o = "other" (non of the graphs), u = upper graph, l = lower graph
        symbols = np.where((graphMatrix[0,:]>0) & (graphMatrix[1,:]>0), "b", np.where((graphMatrix[0,:]==0) & (graphMatrix[1,:]==0), "o", np.where(graphMatrix[0,:]>0,"u","l")))

        plt.plot(trajRight[:,0], trajRight[:,1], 'black')
        plt.plot(trajLeft[:,0], trajLeft[:,1], 'black')

        if colPlot:
            col = np.where(symbols == "b", 'y', np.where(symbols == "o", 'b', np.where(symbols == 'u','r','g')))
            plt.scatter(self.data[:,0],self.data[:,1],c=col, s=2)
            plt.show()

        return symbols
