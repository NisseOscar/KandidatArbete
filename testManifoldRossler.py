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

#----------------------------------------------------------------------
#

eq = Equation.Rossler()
sim = Simulator(eq)

angles = np.linspace(0,2*np.pi,8)

print("Integrating data")
data = sim.states(duration=500)
data = data[10000:]


print("Computing LLE embedding of data")
manifoldData, err = manifold.locally_linear_embedding(data, n_neighbors=12, n_components=2,method = 'hessian') # weird results, can see that it is rossler but it doesn't look as excpected
# Modified provides a smoother manifold, the return map still sucks
# Hessians manifold is weird.... and the return maps suck

print("Done. Reconstruction error: %g" % err)

i = 0

for theta in angles:
    print("\n")
    print("Current angle = " + str(theta))
    spaceVec = np.array([np.cos(theta),np.sin(theta),0])
    planeVec = np.array([np.cos(theta),np.sin(theta)])

    dataMapper = PoincareMapper(spaceVec,data,direction = 1)
    manifoldMapper = PoincareMapper(planeVec,manifoldData,direction = 1)

    print("Computing return maps")
    returnMapData = dataMapper.getValues()
    returnMapOfManifold = manifoldMapper.getValues() # manifold then return map

    returnMapData2 = []

    for point in returnMapData:
        returnMapData2.append([np.sqrt(math.pow(point[0],2)+math.pow(point[1],2)),point[2]])

    print("Computing LLE embedding of return map")
    manifoldOfReturnMap, err = manifold.locally_linear_embedding(returnMapData2,n_neighbors=12,n_components=1) # return map then manifold
    print("Done. Reconstruction error: %g" % err)

    #----------------------------------------------------------------------
    # Plot result

    fig = plt.figure(i)
    i = i + 1

    ax = fig.add_subplot(221, projection='3d')
    ax.plot(data[:, 0], data[:, 1], data[:, 2])
    ax.set_title("Original data")


    ax = fig.add_subplot(222)
    ax.scatter(manifoldOfReturnMap[:-1], manifoldOfReturnMap[1:])
    # plt.axis('tight')
    # plt.xticks([]), plt.yticks([])
    plt.title("Return map of transformed data")


    ax = fig.add_subplot(223)
    ax.plot(manifoldData[:,0],manifoldData[:,1])
    plt.title("Data after embedding")


    ax = fig.add_subplot(224)
    ax.scatter(returnMapOfManifold[:-1],returnMapOfManifold[1:])
    plt.title("Return map of embedded data")


plt.show()
