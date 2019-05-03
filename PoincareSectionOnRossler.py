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

#Loading the data
simData = np.loadtxt('data.txt').T
print(simData)

#Constructing the poincare section
angle = -np.pi/2.7
spaceVec = np.array([np.cos(angle),np.sin(angle),0])
dataMapper = PoincareMapper(spaceVec,simData.T,direction = 1)
returnMapData = dataMapper.iterationdifference()
intersectValues =dataMapper.getValues()

vector2 = np.array([0,0,1])
vector3 = np.cross(spaceVec,vector2)
vector3 = vector3/np.linalg.norm(vector3)

poincmap1 = [np.dot(p,vector3) for p in intersectValues]
poincmap2 = [np.dot(p,vector2) for p in intersectValues]


fig = plt.figure()
ax = fig.add_subplot(121, projection='3d')
ax.plot(simData[0],simData[1],simData[2],linewidth = 0.7,alpha = 0.7)
ax.set_title('The rossler attractor in conjuction with the poincaré section')
#plot plane in figure
xlim = ax.get_xlim().astype(int)
zlim = ax.get_zlim().astype(int)
# Plot plane
xx, zz = np.meshgrid(range(xlim[0],xlim[1]), range(zlim[0],zlim[1]))
yy = (-spaceVec[0]*xx-spaceVec[2]*zz)/spaceVec[1]
ax.plot_surface(xx, yy, zz, alpha=0.2,color = 'k')
insct = np.array(intersectValues).transpose()
# Plot intersecting points
ax.plot(insct[0],insct[1],insct[2],'o',color = 'C0',alpha = 0.9,markersize=3)
ax.set_ylabel('y')
ax.set_xlabel('x')
ax.set_zlabel('z')

ax = fig.add_subplot(122)
ax.scatter(poincmap1,poincmap2,s = 40,alpha=0.7)
ax.set_title('Poincaré map from the poincaré section')
plt.xlim(-10,-19)
ax.set_xlabel('x̂')
ax.set_ylabel('ŷ')

plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(poincmap2[:-1],poincmap2[1:],s = 40,alpha=0.7)
lim = ax.get_xlim()[1]
ax.plot([0,lim],[0,lim],color = 'grey',alpha = 0.35,linewidth = 0.7)
ax.set_title('Returnmap from the poincare map')
ax.set_xlabel('y_0')
ax.set_ylabel('y_1')

plt.show()
