import numpy as np
from math import sin
import math
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from mpl_toolkits.mplot3d import Axes3D
from scipy import signal
import Equation
from scipy.interpolate import splprep as spl
from scipy.interpolate import splev

class Simulator:
    def __init__(self,function,init = 0):
        self.function = function
        self.state0 = function.inCond()

    def states(self,duration=40,split=0.01):
        self.t = np.arange(0.0, duration, split)
        tmp = solve_ivp(self.function.f,[0, duration],self.state0,method='RK45',t_eval=self.t) # RK45, 4th order, 5th order error estimation, without t_eval we get large distances between the points
        # tmp = solve_ivp(self.function.f,[0, duration],self.state0,method='RK45')
        self.data =  tmp.y
        #Return the transpose array of points
        return np.array(self.data).transpose()

    def tredimplot(self,dim = [0,1,2]):
        if self.data is None:
            self.states()
        states = self.data
        fig = plt.figure()
        ax = fig.gca(projection ='3d')
        ax.plot(states[dim[0]], states[dim[1]], states[dim[2]],linewidth=0.5,alpha = 0.9)
        plt.show()
    def twodimplot(self,dim = [0,1]):
        if self.data is None:
            self.states()
        states = self.data
        plt.plot(states[dim[0]], states[dim[1]])
        plt.show()
    def onedimplot(self,dim = [0]):
        if self.data is None:
            self.states()
        states = self.data
        plt.plot(self.t,states[:,dim[0]],alpha = 0.3)
        plt.show()
    def storeData(self,filename = ''):
        np.savetxt(filename+'data.txt',self.data)
        np.savetxt(filename+'Time.txt',self.t)
    def loadData(self,filename):
        self.data = np.loadtxt(filename+'Values.txt')
        self.t = np.loadtxt(filename+'Time.txt')
    def timepoints(self):
        return self.t
    def getData(self):
        return self.data
    def interpolateCurve(self):
        if self.data is None:
            self.states()
        values = np.array(self.data)
        np.swapaxes(values,1,0)
        s = []
        values2 =[]
        lastPoint = values[:,0]
        lastS = 0
        for i, point in enumerate(values[0]):
            point = values[:,i]
            lastS = math.sqrt(np.dot(np.array(point-lastPoint),np.array(point-lastPoint)))+lastS
            s.append(lastS)
            values2.append(point)
            lastPoint = point
        values2 = np.array(values2)
        s2 = np.linspace(s[0],s[-1],round(len(s)/2))
        interpedData = []
        for dim in [0,1,2]:
            data = np.array(values2[:,dim]).reshape(len(s),1).squeeze()
            dimData = []
            s2Index = 0
            lastIndex = 0
            for i, value in enumerate(data):
                if i % 10 == 0 and i+10 < len(s):
                    tck, u = spl(np.array(data[i:i+9]).reshape(1,9),u = np.array(s[i:i+9]).reshape(9,1).flatten(),k = 5)
                    while s2[s2Index] < s[i+9]:
                        s2Index +=1
                    if s2Index != lastIndex:
                        newValues = splev(s2[lastIndex:s2Index],tck)
                        for xi in newValues:
                            for xij in xi:
                                dimData.append(xij)
                    lastIndex = s2Index
            interpedData.append(dimData)
        interpedData = np.array(interpedData)
        return interpedData.transpose()
