import numpy as np
from math import sin
import math
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
from scipy import signal
from scipy.integrate import solve_ivp
import Equation

class Simulator:
    def __init__(self,function,init = 0):
        self.function = function
        self.state0 = init

    def states(self,duration,split):
        self.t = np.arange(0.0, duration, split)
        self.states = odeint(self.function.f, self.state0, self.t) # Choose integrator
        #self.states = solve_ivp(self.function,[0, duration],self.state0,method='RK45',t_eval=self.t) # RK45, 4th order, 5th order error estimation
        return self.states

    def tredimplot(self,dim = [0,1,2]):
        if self.states is None:
            self.states()
        states = self.states
        fig = plt.figure()
        ax = fig.gca(projection ='3d')
        ax.plot(states[:,dim[0]], states[:,dim[1]], states[:,dim[2]],linewidth=0.5,alpha = 0.9)
        #ax.plot(t,self.states[:,2])
        plt.show()
    def twodimplot(self,dim = [0,1]):
        if self.states is None:
            self.states()
        states = self.states
        plt.plot(states[:,dim[0]], states[:,dim[1]])
        plt.show()
    def onedimplot(self,dim = [0]):
        if self.states is None:
            self.states()
        states = self.states
        plt.plot(self.t,states[:,dim[0]],alpha = 0.3)
        plt.show()
<<<<<<< HEAD
    def saveData(self):
        if self.states is None:
            self.states()
        np.savetxt("data.txt",self.states)
eq = Equation.Rossler()
sim = Simulator(function = eq,init = [1.0,8,1.0])
state = sim.states(600,0.01)
sim.saveData()
=======
    def storeData(self,filename):
        np.savetxt(filename+'Values.txt',self.states)
        np.savetxt(filename+'Time.txt',self.t)
    def loadData(self,filename):
        self.states = np.loadtxt(filename+'Values.txt')
        self.t = np.loadtxt(filename+'Time.txt')

#eq = Equation.Fitz()
#sim = Simulator(eq,init = eq.inCond())
#state = sim.states(4000,0.01)
#sim.onedimplot(dim = [1])
>>>>>>> 1a7790caaec21a47f977dd4c7f8e8ad219db1797
