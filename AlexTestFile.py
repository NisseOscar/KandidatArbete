import Equation
from Simulator import Simulator
from DimensionalityFinder import DimensionalityFinder
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.integrate import odeint
from scipy.integrate import solve_ivp

eq = Equation.Fitz()
sim = Simulator(eq)
# data = sim.states(duration=100, split = 0.01) # 40  -> 1.369, 400 -> 1.497

state0 = [0.01,0.01,0.01,0.01]
t = np.linspace(0,10000,50000)
# sim = Simulator(eq)
#
# data = sim.states(duration = 300011, split = 0.25)
# data = sim.interpolateCurve()[10000:]
# print(data.shape)
n = 2
a = [-0.025794, -0.025794]
b = [0.0065, 0.0135]
c = [0.02, 0.02]
k = 0.128
A =[[0,1],[1,0]]
def f(state,t):
    x = state[0:n]
    y = state[n:2*n]# unpack the state vector
    xdot = np.multiply(x,np.multiply(a-x,x-np.ones(n)))-y+k*(np.matmul(A,x)-x)
    y = np.multiply(b,x)-np.multiply(c,y)
    state[0:n] = xdot
    state[n:2*n] = y
    return state
data = odeint(f, state0, t)

fig = plt.figure(0)

ax = fig.add_subplot(131)
ax.set_title('Ocillator 1')
ax.plot(data[:,0],data[:,2])

ax = fig.add_subplot(132)
ax.set_title('Ocillator 2')
ax.plot(data[:,1],data[:,3])

ax = fig.add_subplot(133)
ax.set_title('Y1 and Y2 over time')
ax.plot(t,data[:,2])
ax.plot(t,data[:,3],c='r', alpha = 0.6)

fig = plt.figure(1)

data = sim.states(duration=10000, split = 0.2) # 40  -> 1.369, 400 -> 1.497

ax = fig.add_subplot(131)
ax.set_title('Ocillator 1')
ax.plot(data[:,0],data[:,2])

ax = fig.add_subplot(132)
ax.set_title('Ocillator 2')
ax.plot(data[:,1],data[:,3])

ax = fig.add_subplot(133)
ax.set_title('Y1 and Y2 over time')
ax.plot(sim.t,data[:,2])
ax.plot(sim.t,data[:,3],c='r', alpha = 0.6)

fig = plt.figure(2)

def f(t,state):
    x = state[0:n]
    y = state[n:2*n]# unpack the state vector
    xdot = np.multiply(x,np.multiply(a-x,x-np.ones(n)))-y+k*(np.matmul(A,x)-x)
    y = np.multiply(b,x)-np.multiply(c,y)
    state[0:n] = xdot
    state[n:2*n] = y
    return state

t = np.linspace(0,10000,50000)
tmp = solve_ivp(f,[0, 10000],state0,method='RK23',t_eval=t)

ax = fig.add_subplot(131)
ax.set_title('Ocillator 1')
ax.plot(data[:,0],data[:,2])

ax = fig.add_subplot(132)
ax.set_title('Ocillator 2')
ax.plot(data[:,1],data[:,3])

ax = fig.add_subplot(133)
ax.set_title('Y1 and Y2 over time')
ax.plot(sim.t,data[:,2])
ax.plot(sim.t,data[:,3],c='r', alpha = 0.6)


plt.show()

#
# finder = DimensionalityFinder(data)
# dim = finder.calculateCorrelationDimension()
#
# print("Dimension = " +str(dim))
