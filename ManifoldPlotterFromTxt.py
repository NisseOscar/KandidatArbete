import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
from sklearn import manifold, datasets
from Simulator import Simulator
from PoincareMapper import PoincareMapper
from colorPlot import ColorPlot
import Equation
import math
import numpy as np

start = 1000;
# Initiate arrays
print('Loading data')
manData = np.loadtxt('TSNEData.txt')[start:]
simData = np.loadtxt('Data.txt')
simData = (simData[start:]).T

# Colormapper
print('Constructing colorschema' )
colorplot = ColorPlot(manData = manData, simData = simData)
colormap = colorplot.getColorMap()

# Create manifolder for poincare maps
print('Creating embedding')
embedding= manifold.TSNE(n_components=1, init='pca', random_state=0)

#-------------------------------------------------------------------
# -----------------Plotting-----------------------------------------
#-------------------------------------------------------------------
# Choose angle from x-axis for poincaremap
print('Constructing planevectors')
angle = -np.pi/2.7
spaceVec = np.array([np.cos(angle),np.sin(angle),0])
planeVec = np.array([np.cos(angle),np.sin(angle)])

#Make poincaremapper
print('Making poincareMappers')
dataMapper = PoincareMapper(spaceVec,simData.T,direction = 1)
manifoldMapper = PoincareMapper(planeVec,manData,direction = 1)

# Create returnmap of poincare sectionand conduct the manifold on it.
print('Constructing plane intersections')
def func(arr):
    return arr[2]
returnMapData = dataMapper.iterationdifference(func = func)
intersectValues =dataMapper.getValues()
returnMapOfManifold = manifoldMapper.iterationdifference()
intsctIndx = dataMapper.getIntersctIndx()
returnMapColor = [colormap[i] for i in intsctIndx[0:-1] ]#Not last index since we remove it

#----------------------------------------------------------------------
# Plot result
fig = plt.figure()
# Original simulation data
print('Plotting Rossler equation')
ax = fig.add_subplot(221, projection='3d')
colorplot.plotSim(ax)
ax.set_title("Original data")
#plot plane in figure
xlim = ax.get_xlim().astype(int)
zlim = ax.get_zlim().astype(int)
# Plot plane
xx, zz = np.meshgrid(range(xlim[0],xlim[1]), range(zlim[0],zlim[1]))
yy = (-spaceVec[0]*xx-spaceVec[2]*zz)/spaceVec[1]
ax.plot_surface(xx, yy, zz, alpha=0.2,color = 'k')
insct = np.array(intersectValues).transpose()
# Plot intersecting points
ax.plot(insct[0],insct[1],insct[2],'o',color = 'red',alpha = 0.7,markersize=0.4)
ax.set_ylabel('y')
ax.set_xlabel('x')
ax.set_zlabel('z')

# Original poincare map from simulation
print('Plotting returnmap of poincaresection')
ax = fig.add_subplot(222)
ax.scatter(returnMapData[:-1], returnMapData[1:],c =returnMapColor)
plt.title("Return map of Poincare map")
ax.set_ylabel('z1')
ax.set_xlabel('z0')

# Data after manifold
print('Plotting manifold')
ax = fig.add_subplot(223)
colorplot.plotMan(ax)
plt.title("Data after embedding")
left,right = ax.get_xlim()
plx = range(int(left),int(right))
ply = planeVec[1]/planeVec[0] * plx
ax.plot(plx,ply,'-',alpha = 0.3,color = 'k')
ax.set_ylabel('y')
ax.set_xlabel('x')

# ReturnMap of the manifold
print('Plotting returnmap of manifold of the poincaresection')
ax = fig.add_subplot(224)
ax.scatter(returnMapOfManifold[:-1],returnMapOfManifold[1:],c =returnMapColor)
plt.title("Return map of poincare section on embedded data")
ax.set_ylabel('z1')
ax.set_xlabel('z0')

plt.show()
