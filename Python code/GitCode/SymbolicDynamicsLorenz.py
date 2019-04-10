import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

# This import is needed to modify the way figure behaves
from mpl_toolkits.mplot3d import Axes3D
Axes3D
from sklearn import manifold, datasets
from Simulator import Simulator
from PoincareMapper import PoincareMapper
import Equation
import math
from SymbolicDynamics import *
# Create data
eq = Equation.Lorentz()
sim = Simulator(eq)
data = sim.states(duration=200,split = 0.01) # max modified 850
data = data[1000:]
data = sim.interpolateCurve()[1000:]

# Create modified data
r =np.sqrt(np.square(data[:, 0])+np.square(data[:, 1]))
dataMod = np.zeros(np.shape(data))
dataMod[:,0] = (np.square(data[:, 0])-np.square(data[:, 1]))/r
dataMod[:,1] = 2*data[:, 0]*data[:, 1]/r
dataMod[:,2] = data[:, 2]

# Plot original


# Compute return maps
angles = np.linspace(0,2*np.pi,8)
i=0
for theta in angles:
    spaceVec = np.array([np.cos(theta),np.sin(theta),0])
    planeVec = np.array([np.cos(theta),np.sin(theta)])
    dataMapper = PoincareMapper(spaceVec,data,direction = 1)
    dataModMapper = PoincareMapper(spaceVec,dataMod,direction = 1)
    print("Computing return map")
    returnMapData = dataMapper.getValues()
    print("Computing return map modified")
    returnMapDataMod = dataModMapper.getValues()
    returnMapData2 = []
    returnMapDataMod2 = []

    print("Append")
    for point in returnMapData:
        returnMapData2.append([np.sqrt(math.pow(point[0],2)+math.pow(point[1],2)),point[2]])

    for point in returnMapDataMod:
        returnMapDataMod2.append([np.sqrt(math.pow(point[0],2)+math.pow(point[1],2)),point[2]])

    returnMapData2 = np.array(returnMapData2)
    returnMapDataMod2 = np.array(returnMapDataMod2)
    #manifoldOfReturnMapMod = manifold.Isomap(n_neighbors=12, n_components=1).fit_transform(returnMapDataMod2)
    manifoldOfReturnMapMod = manifold.MDS(n_components=1).fit_transform(returnMapDataMod2)

    i=i+1
    fig = plt.figure(i)
    # Plot data
    ax = fig.add_subplot(231, projection='3d')
    ax.plot(data[:, 0], data[:, 1], data[:, 2],alpha = 0.8, linewidth = 0.3)
    returnMapData = np.array(returnMapData)
    ax.scatter(returnMapData[:,0],returnMapData[:,1],returnMapData[:,2],c='r',s=2)
    ax.set_title("Original data")

    # Plot modified
    ax = fig.add_subplot(232, projection='3d')
    ax.plot(dataMod[:, 0], dataMod[:, 1], dataMod[:, 2],alpha = 0.8, linewidth = 0.3)
    returnMapDataMod = np.array(returnMapDataMod)
    ax.scatter(returnMapDataMod[:,0],returnMapDataMod[:,1],returnMapDataMod[:,2],c='r',s=2)
    ax.set_title("Modified data")

    # Plot return map of data
    ax = fig.add_subplot(233)
    ax.scatter(returnMapData2[:-1,0],returnMapData2[1:,0],s=2)
    ax.set_title("Return map of data")

    # Plot return map of reembedded modified data
    ax = fig.add_subplot(234)
    z = SymbolicDynamics.symbolicRepresentation(manifoldOfReturnMapMod[:-1],manifoldOfReturnMapMod[1:])
    #print(z[:10])
    col =  np.where(z < 1, 'y', 'b')
    ax.scatter(manifoldOfReturnMapMod[:-1], manifoldOfReturnMapMod[1:],c=col,s=2)
    ax.set_title("Return map of reembedded modified data")

    # Plot radial return map of modified data
    ax = fig.add_subplot(235)
    z = SymbolicDynamics.symbolicRepresentation(returnMapDataMod2[:-1,0],returnMapDataMod2[1:,0])
    #print(z[:10])
    col =  np.where(z < 1, 'y', 'b')
    ax.scatter(returnMapDataMod2[:-1,0],returnMapDataMod2[1:,0],c=col,s=2)
    ax.set_title("Return map of modified data, radial")

    # Plot vertical return map of modified data
    ax = fig.add_subplot(236)
    z = SymbolicDynamics.symbolicRepresentation(returnMapDataMod2[:-1,1],returnMapDataMod2[1:,1])
    #print(z[:10])
    col =  np.where(z < 1, 'y', 'b')
    ax.scatter(returnMapDataMod2[:-1,1],returnMapDataMod2[1:,1],c=col,s=2)
    ax.set_title("Return map of modified data, vertical")

    fig.suptitle("theta = " + str(theta))
plt.show()
