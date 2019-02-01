import numpy as np
from math import sin
import math
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
from scipy import signal

class PoincareMapper:
    def __init__(self,plane,array):
        self.array = array
        self.plane = plane
        u1 = np.array([-plane[1],1,0])
        v2 = np.array([-plane[2],0,1])
        e1 = np.linalg.norm(u1)*u1
        u2 = v2 - np.dot(u1,v2)/np.dot(u1,u1)*u1
        e2 = np.linalg.norm(u2)*u2
        self.matrix = np.array([e1,e2])
    def crossing(self,x1,x2):
        return np.dot(x1,self.plane)*np.dot(x2,self.plane)<0
    def projection(self,x1,x2):
        d1 = np.dot(x1,self.plane)
        d2 = np.dot(x2,self.plane)
        return (d1*x1+d2*x2)/(d1+d2)
    def map(self):
        values = []
        for i in range(len(self.array)-1):
            x1 = self.array[i]
            x2 = self.array[i+1]
            if(self.crossing(x1,x2)):
                nearestPoint = self.projection(x1,x2)
                values.append(self.matrix.dot(nearestPoint))
        return np.asarray(values)
rho = 26.0
sigma = 10.0
beta = 8.0 / 3.0
def f(state, t):
  x, y, z = state  # unpack the state vector
  return sigma * (y - x), x * (rho - z) - y, x * y - beta * z  # derivatives
state0 = [1.0, 1.0, 1.0]
t = np.arange(0.0, 40.0, 0.01)
states = odeint(f, state0, t)

mapper = PoincareMapper(np.array([0,1,0]),states)
values = mapper.map()
print(values)
plt.plot(values[:,0],values[:,1],'o')
plt.show()
