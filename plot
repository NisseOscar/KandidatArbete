import numpy as np
import numpy.linalg as lin
import Equation
from colorPlot import ColorPlot
import matplotlib.pyplot as plt
import math
from collections import deque
import PoincareMapper


################# Plotting #######################
simData = np.loadtxt('Data.txt').T
poincare =1
colorplot = ColorPlot(simData= simData)
spaceVec = ([ 0.39079842 ,-0.91990542, -0.0324133 ])
fig = plt.figure()
print('Plotting Rossler equation')
ax = plt.gca(projection='3d')
#colormap.plot(ax)
ax.plot(simData[0],simData[1],simData[2])
ax.set_title("Automaticly generated poincare section")



# Plot plane
xlim = ax.get_xlim().astype(int)
zlim = ax.get_zlim().astype(int)
xx, zz = np.meshgrid(range(xlim[0],xlim[1]), range(zlim[0],zlim[1]))
yy = (-spaceVec[0]*xx-spaceVec[2]*zz)/spaceVec[1]
ax.plot_surface(xx, yy, zz, alpha=0.2,color = 'k')
#insct = np.array(intersectValues).transpose()
# Plot intersecting points
# ax.plot(insct[0],insct[1],insct[2],'o',color = 'red',alpha = 0.7,markersize=0.4)
ax.set_ylabel('y')
ax.set_xlabel('x')
ax.set_zlabel('z')

plt.show()
