import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

# based on https://scikit-learn.org/dev/auto_examples/manifold/plot_swissroll.html#sphx-glr-auto-examples-manifold-plot-swissroll-py

# This import is needed to modify the way figure behaves
from mpl_toolkits.mplot3d import Axes3D
Axes3D
from sklearn import manifold, datasets
from Simulator import Simulator
from PoincareMapper import PoincareMapper
import Equation
import math
from SymbolicDynamics import *

#----------------------------------------------------------------------
#

eq = Equation.Rossler()
sim = Simulator(eq)
angles = np.linspace(0,2*np.pi,10)

#print("Integrating data")
# data = sim.states(duration=500)
data = sim.states(duration=150,split = 0.01) # max modified 850
data = data[1000:]
data = sim.interpolateCurve()[1000:]

# print("Loading data")
# sim.loadData("TestRossler")
# data = sim.getData()
# manifoldData = np.loadtxt("ManifoldRossler.txt")

#print("Computing LLE embedding of data")
#manifoldData, err = manifold.locally_linear_embedding(data, n_neighbors=12, n_components=2,method = 'standard') # weird results, can see that it is rossler but it doesn't look as excpected
manifoldData = manifold.Isomap(n_neighbors =12, n_components=2).fit_transform(data)
#print(manifoldData)
i = 0

for theta in angles:
    #print("\n")
    #print("Current angle = " + str(theta))
    spaceVec = np.array([np.cos(theta),np.sin(theta),0])
    planeVec = np.array([np.cos(theta),np.sin(theta)])

    dataMapper = PoincareMapper(spaceVec,data,direction = 1)
    manifoldMapper = PoincareMapper(planeVec,manifoldData,direction = 1)

    #print("Computing return maps")
    returnMapData = dataMapper.getValues()
    returnMapOfManifold = manifoldMapper.getValues() # manifold then return map
    indexReturnMapOfManifold = manifoldMapper.getIntersctIndx()
    returnMapData2 = []
    returnMapOfManifold2 = []

    for point in returnMapData:
        returnMapData2.append([np.sqrt(math.pow(point[0],2)+math.pow(point[1],2)),point[2]])

    for point in returnMapOfManifold:
        returnMapOfManifold2.append(math.sqrt(point[0]**2+point[1]**2)) # not working when just loading data

    #print("Computing LLE embedding of return map")
    #manifoldOfReturnMap, err = manifold.locally_linear_embedding(returnMapData2,n_neighbors=12,n_components=1) # return map then manifold
    manifoldOfReturnMap = manifold.Isomap(n_neighbors=12, n_components=1).fit_transform(returnMapData2)
    #print("Done. Reconstruction error: %g" % err)

    #----------------------------------------------------------------------
    # Plot result

    fig = plt.figure(i)
    i = i + 1
    returnMapData = np.array(returnMapData)
    ax = fig.add_subplot(221, projection='3d')
    ax.plot(data[:, 0], data[:, 1], data[:, 2],alpha = 0.8, linewidth = 0.3)
    ax.scatter(returnMapData[:,0],returnMapData[:,1],returnMapData[:,2],c='r',s=4)
    ax.set_title("Original data")

    ax = fig.add_subplot(222)
    z = SymbolicDynamics.symbolicRepresentation(manifoldOfReturnMap[:-1],manifoldOfReturnMap[1:])
    print(z)
    #z = np.array(z)
    col =  np.where(z < 1, 'y', 'b')
    ax.scatter(manifoldOfReturnMap[:-1], manifoldOfReturnMap[1:], c=col, s = 5)
    plt.title("Return map of reembedded Poincaré section")

    returnMapData2 = np.array(returnMapData2)
    ax = fig.add_subplot(223)
    z = SymbolicDynamics.symbolicRepresentation(returnMapData2[:-1,0],returnMapData2[1:,0])
    #print(z)
    #z = np.array(z)
    col =  np.where(z < 1, 'y', 'b')
    ax.scatter(returnMapData2[:-1,0],returnMapData2[1:,0], c=col, s=5)
    plt.title("Return map, radial")

    ax = fig.add_subplot(224)
    ax.scatter(returnMapData2[:-1,1],returnMapData2[1:,1])
    plt.title("Return map, vertical")

plt.show()
