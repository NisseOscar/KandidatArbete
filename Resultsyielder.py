import numpy as np
from sklearn import manifold, datasets
#from ../colorPlot import ColorPlot
import math
from Simulator import Simulator
from PoincareMapper import PoincareMapper
import Equation
import matplotlib.colors as colors
import matplotlib.cm as cm

import matplotlib.pyplot as plt

eq = Equation.Rossler()
sim = Simulator(eq)

fig = plt.figure()

data = sim.states(duration=400.1,split = 0.05)[2000:]
data = sim.interpolateCurve()[1000:]

colmap = cm.get_cmap('plasma')
#Rossler
rossnorm = colors.Normalize(vmin=min(data.T[2]), vmax=max(data.T[2]))
col = [colmap(rossnorm(value)) for value in data.T[2]]
# data = sim.interpolateCurve()[1000:]


for i in range(4,14,2):
    # print("Integrating data")
    # data = sim.states(duration=400.1,split = (0.2-0.02*i))
    # data = sim.interpolateCurve()[1000:]


    print("Computing embedding of data")
    emb = manifold.LocallyLinearEmbedding(n_neighbors = i, n_components=2,method = 'standard',eigen_solver='auto').fit_transform(data)
    ax = fig.add_subplot(149+i/2)
    ax.scatter(emb[:,0],emb[:,1],c = col, s =10,alpha=0.7)
    plt.title(str(i) + ' neighbours' )
    # ax.xaxis.set_major_formatter(NullFormatter())
    # ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')

plt.show()


#embedding= manifold.TSNE(n_components=2,init= 'pca').fit_transform(data)
#manifoldData = embedding.fit_transform(data)
