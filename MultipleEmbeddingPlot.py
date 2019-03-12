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

data = sim.states(duration=500)
data = data[10000:]
dataArr = [data[::50], data[::40], data[::30], data[::20]]
neighbors = range(6,16,2)
n_datapoints = [len(dataArr[0][:,0]), len(dataArr[1][:,0]), len(dataArr[2][:,0]), len(dataArr[3][:,0])]
nbr_dataSets = len(n_datapoints)
print(str(nbr_dataSets))
nbr_neighborSets = len(neighbors)
print(str(nbr_neighborSets))

fig = plt.figure()
for i in range(10):
    #manifoldData = manifold.MDS(n_components=2, max_iter=100, n_init=1).fit_transform(data)
    #manifoldData, err = manifold.locally_linear_embedding(data, n_neighbors= neighbors[i%5], n_components=2,method = 'hessian') # weird results, can see that it is rossler but it doesn't look as excpected
    manifoldData = manifold.Isomap(n_neighbors=neighbors[i%nbr_neighborSets], n_components=2).fit_transform(dataArr[i%nbr_dataSets])
    ax = fig.add_subplot(nbr_neighborSets,nbr_dataSets,i+1)
    ax.plot(manifoldData[:,0],manifoldData[:,1])
    plt.title("k = " + str(neighbors[i%nbr_neighborSets]) + ", N = " + str(n_datapoints[i%nbr_dataSets]))


plt.show()
