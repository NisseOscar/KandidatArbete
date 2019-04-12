from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KDTree
import matplotlib.pyplot as plt
import numpy as np
from queue import Queue

class NearestNeighbor:
    def __init__(self, data, n_neighbors, graphIndex):
        self.data = data
        self.n_neighbors = n_neighbors
        self.graphIndex = graphIndex
    def SeperateGraphs(data, n_neighbors, graphIndex):
        # Find the nearest neighbors for each data point
        nbrs = NearestNeighbors(n_neighbors, algorithm='ball_tree').fit(data)
        distances, indices = nbrs.kneighbors(data)
        startPoints = [None] *2*len(graphIndex)

        for i in range(0,len(graphIndex)):
            # TODO loopa över fler grannar, välj den som ligger närmst i x led
            start1 = graphIndex[i,]
            dist = data[indices[graphIndex[i],1:],0] #-data[graphIndex[i,0],0]
            distIndex = indices[graphIndex[i],1:]
            minX = np.argmin(np.abs(data[graphIndex[i],0]-dist))
            start2 = indices[distIndex[minX],0]
            if data[start1,0] <= data[start2,0]:
                startPoints[2*i] = start1
                startPoints[2*i+1] = start2
            else:
                startPoints[2*i] = start2
                startPoints[2*i+1] = start1
        n_graphs = len(startPoints)
        n_dataPoints = len(indices)
        graphArray = np.zeros((n_graphs, n_dataPoints))
        #Create graphs
        for i in range(0,n_graphs):
            current = startPoints[i]
            graphArray[i,current] = 1
            que = Queue(n_dataPoints)
            que.put(current)
            #Until all neighbors are added to the graph
            while not que.empty():
                current = que.get()
                for j in range(1,n_neighbors):
                    if graphArray[i,indices[current,j]] == 0:
                        if i % 2 == 0 and data[indices[current,j],0] < data[current,0]:
                            que.put(indices[current,j])
                            graphArray[i,indices[current,j]] = 1
                        elif i % 2 == 1 and data[indices[current,j],0] > data[current,0]:
                            que.put(indices[current,j])
                            graphArray[i,indices[current,j]] = 1
        gM = np.zeros((2,len(data[:,0])))
        gM[0,:] = graphArray[0,:] + graphArray[1,:]
        gM[1,:] = graphArray[2,:] + graphArray[3,:]
        symbols = np.where((gM[0,:]>0) & (gM[1,:]>0), "b", np.where((gM[0,:]==0) & (gM[1,:]==0), "o", np.where(gM[0,:]>0,"u","l")))

        return symbols
