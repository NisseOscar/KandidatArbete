import numpy as np
from math import sin
import math
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
from scipy import signal
from mpl_toolkits import mplot3d


a = 0.2
b = 0.2
c = 5.7

def rossler(state,t):
    x,y,z = state
    return - y - z, x + a * y , b + z * ( x - c )

a1 = -0.025794
a2 = -0.025794
b1 =  0.0065
b2 =  0.0135
c1 = 0.02
c2 = 0.02
k = 0.128

def fitz(state,t):
    x1,y1,x2,y2 = state
    return x1 * (a1 - x1) * (x1 - 1) - y1 + k * (x2 - x1) , b1 * x1 - c1 * y1 , x2 * (a2 - x2) * (x2-1) - y2 + k * (x1 - x2), b2 * x2 - c2 * y2

state0 = [0.01, 0.01, 0.01, 0.01]
t = np.arange(0.0, 10000.0, 0.01)
states = odeint(fitz, state0, t)

fig = plt.figure()
plt.plot(t*0.01,states[:,1], linewidth =0.2)
plt.xlabel('Time')
plt.ylabel('Amplitude')
#plt.axis('off')
plt.show()
