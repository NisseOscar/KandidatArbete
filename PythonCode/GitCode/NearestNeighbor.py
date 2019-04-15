from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KDTree
import matplotlib.pyplot as plt
import numpy as np
from queue import Queue

class NearestNeighbor:
    def __init__(self, data, n_neighbors):
        self.data = data
        self.n_neighbors = n_neighbors

    def findstartIndex(self, graphArray):
        # Find max data point that has not already been graphed
        dataNotGraphed = np.where(graphArray < 1, self.data[:,1], np.NINF)
        startIndex = np.argmax(dataNotGraphed)
        return startIndex

    def ConstructGraph(self, indices, startIndex):

        # 1 if point belongs to the graph, 0 otherwise
        graphArray = np.zeros(len(self.data))

        for i in range(0,2):
            current = startIndex
            graphArray[current] = 1
            queueNeighbors = Queue(len(self.data))
            queueNeighbors.put(current)

            # Continue as long as the points have neighbors further down the branch
            while not queueNeighbors.empty():
                current = queueNeighbors.get()
                for j in range(1,self.n_neighbors):
                    # Do only add if not already added
                    if graphArray[indices[current,j]] == 0:

                        # Left branch, only add if the point is further down the branch
                        if i % 2 == 0 and self.data[indices[current,j],0] < self.data[current,0]:
                            queueNeighbors.put(indices[current,j])
                            graphArray[indices[current,j]] = 1

                        # Right branch, only add if the point is further down the branch
                        elif i % 2 == 1 and self.data[indices[current,j],0] > self.data[current,0]:
                            queueNeighbors.put(indices[current,j])
                            graphArray[indices[current,j]] = 1
        return graphArray

    def SeperateGraphs(self, colPlot):
        # Find the nearest neighbors for each data point
        nbrs = NearestNeighbors(self.n_neighbors, algorithm='ball_tree').fit(self.data)
        distances, indices = nbrs.kneighbors(self.data)

        # 1 if data point j belongs to graph i, zero otherwise. i in nbr graphs, j in nbr datapoints
        graphMatrix = np.zeros((2,len(self.data)))

        # Find start points for Upper graph
        startIndexUpperGraph = self.findstartIndex(graphMatrix[0,:])

        # Construct Upper graph
        graphMatrix[0,:] = self.ConstructGraph(indices, startIndexUpperGraph)

        # Find start points for lower graph
        startIndexLowerGraph = self.findstartIndex(graphMatrix[0,:])

        # Construct lower graph
        graphMatrix[1,:] = self.ConstructGraph(indices, startIndexLowerGraph)

        # Gives each data point a different symbol depending on if it belongs to the Upper graph, lower graph, both graphs or non of the graphs
        # b = both graphs, o = "other" (non of the graphs), u = upper graph, l = lower graph
        symbols = np.where((graphMatrix[0,:]>0) & (graphMatrix[1,:]>0), "b", np.where((graphMatrix[0,:]==0) & (graphMatrix[1,:]==0), "o", np.where(graphMatrix[0,:]>0,"u","l")))

        if colPlot:
            fig = plt.figure()
            col = np.where(symbols == "b", 'y', np.where(symbols == "o", 'b', np.where(symbols == 'u','r','g')))
            plt.scatter(self.data[:,0],self.data[:,1],c=col, s=2)
            plt.show()

        return symbols
