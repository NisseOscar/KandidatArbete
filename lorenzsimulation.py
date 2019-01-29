import numpy as np
from math import sin
import math
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
from scipy import signal

rho = 26.0
sigma = 10.0
beta = 8.0 / 3.0


def f(state, t):
  x, y, z = state  # unpack the state vector
  return sigma * (y - x), x * (rho - z) - y, x * y - beta * z  # derivatives

state0 = [1.0, 1.0, 1.0]
t = np.arange(0.0, 400.0, 0.01)
states = odeint(f, state0, t)

fig = plt.figure()
ax = fig.gca(projection ='3d')
ax.plot(states[:,0], states[:,1], states[:,2])
#ax.plot(t,states[:,2])
plt.show()


z = np.r_[True, states[1:,2] < states[:-1,2]] & np.r_[states[:-1,2] < states[1:,2], True]
z = z*states[:,2]
z = z[np.nonzero(z)]
z1 = z[:-1]
z2 = z[1:]

plt.plot(z1,z2,'ro')
plt.plot()
plt.show()
