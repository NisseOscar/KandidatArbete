import numpy as np
from math import sin
import math
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
from scipy import signal
import Equation

class Simulator:
    def __init__(self,function,init = 0):
        self.function = function
        self.state0 = function.inCond()

    def states(self,duration=40,split=0.01):
        self.t = np.arange(0.0, duration, split)
        self.states = odeint(self.function.f, self.state0, self.t) # Choose integrator
        return self.states

    def tredimplot(self,dim = [0,1,2]):
        if self.states is None:
            self.states()
        states = self.states
        fig = plt.figure()
        ax = fig.gca(projection ='3d')
        ax.plot(states[:,dim[0]], states[:,dim[1]], states[:,dim[2]],linewidth=0.5,alpha = 0.9)
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
    def storeData(self,filename):
        np.savetxt(filename+'Values.txt',self.states)
        np.savetxt(filename+'Time.txt',self.t)
    def loadData(self,filename):
        self.states = np.loadtxt(filename+'Values.txt')
        self.t = np.loadtxt(filename+'Time.txt')
