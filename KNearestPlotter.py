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

simData = np.loadtxt('largedata.txt')

fig = plt.figure()
for j in range(1,3):
    data = simData[0::(10**j)]
    fig = plt.figure()
    for i in range(6,14,2):
        embedding= manifold.LocallyLinearEmbedding(n_neighbors = i, n_components=2,method='ltsa',eigen_solver='auto').fit_transform(data)
        ax = fig.add_subplot(525 + i)
        plt.title('k is: '+ str(i) +' We have: '+str(500/(1-0.1*j)) + ' datapoints')
        ax.plot(embedding)
    plt.show()
