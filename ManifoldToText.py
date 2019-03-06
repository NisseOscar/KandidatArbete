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
import numpy as np
#----------------------------------------------------------------------
#

eq = Equation.Rossler()
sim = Simulator(eq)

angles = np.linspace(0,2*np.pi,8)

print("Integrating data")
data = sim.states(duration=500)[10000:]
np.savetxt('data.txt',data)


print("Computing embedding of data")
embedding= manifold.TSNE(n_components=2, init='pca', random_state=0)
manifoldData = embedding.fit_transform(data)
np.savetxt('TSNEData.txt',manifoldData)
print(len(data))
print(len(manifoldData))


# Modified provides a smoother manifold, the return map still sucks
# Hessians manifold is weird.... and the return maps suck
