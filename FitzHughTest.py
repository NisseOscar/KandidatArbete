import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn import manifold, datasets
from Simulator import Simulator
from PoincareMapper import PoincareMapper
import Equation
import math
from scipy.integrate import odeint
from FitzSimulator import FitzSimulator


fitz = FitzSimulator(n=2)
print('Simulating system')
data = fitz.states(duration = 5000, split = 0.01, rtol = 1.49012e-9, atol = 1.49012e-9)
print('Interpolating curve')
data = fitz.interpolateCurve()[1000:]
np.savetxt('Fitz2Data.txt',data)

# print('Starting analysis')
# n = 8
# interval = math.floor(data.shape[0]/n)
#
# for i in range(0,n):
#     print('Interval %g' % i)
#     manifoldData, err = manifold.locally_linear_embedding(data[i*interval:(i+1)*interval], n_neighbors=12, n_components=2,method = 'modified') # weird results, can see that it is rossler but it doesn't look as excpected
#     print("Done. Reconstruction error: %g" % err)
#
#     fig = plt.figure(i)
#
#     ax = fig.add_subplot(131)
#     ax.set_title('Oscillator 1')
#     ax.plot(data[i*interval:(i+1)*interval,0],data[i*interval:(i+1)*interval,2])
#
#     ax = fig.add_subplot(132)
#     ax.set_title('Oscillator 2')
#     ax.plot(data[i*interval:(i+1)*interval,1],data[i*interval:(i+1)*interval,3])
#
#     ax = fig.add_subplot(133)
#     ax.set_title('Reembedded system')
#     ax.plot(manifoldData[:,0],manifoldData[:,1])
#
# plt.show()
