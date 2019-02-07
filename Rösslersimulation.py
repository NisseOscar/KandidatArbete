import numpy as np
from math import sin
import math
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
from scipy import signal


a = 0.1
b = 0.1
c = 14

def f(state, t):
  x, y, z = state  # unpack the state vector
  return -y-z, x+a*y,b+z*(x-c) # derivatives

state0 = [1.0, 1.0, 1.0]
t = np.arange(0.0, 400.0, 0.01)
states = odeint(f, state0, t)

fig = plt.figure()
ax = fig.gca(projection ='3d')
ax.plot(states[:,0], states[:,1], states[:,2],'r-',alpha = 0.6)
ax.grid(True)
ax.axes.get_yaxis().set_visible(False)
ax.axes.get_xaxis().set_visible(False)
#ax.plot(t,states[:,2])
plt.show()
