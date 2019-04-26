import Equation
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.interpolate import splprep as spl
from scipy.interpolate import splev

class FitzSimulator:

    def __init__(self,inCond = None, n=2,a = -0.025794,c=0.02,b = None,A = None,k=0.128):
        self.n = n
        self.k = k
        if(isinstance(a,float)):
            self.a = a*np.ones(n)
        else:
            self.a = a,
        if(isinstance(c,float)):
            self.c = c*np.ones(n)
        else:
            self.c = c
        if(A is None):
            self.A = np.ones((n,n))-np.identity(n)
        if(b is None):
            self.b = np.linspace(0.006,0.014,n)
        else:
            self.b = b;            
        if inCond is None:
            self.inCond = 0.01001*np.ones(2*self.n)
        else:
            self.inCond = inCond

    def states(self, duration = 1000, split = 0.1, rtol = 1.49012e-8, atol = 1.49012e-8):
        self.t = np.arange(0,duration, split)
        self.states = odeint(self.f,self.inCond,self.t, rtol = rtol, atol = atol)
        return self.states

    def f(self,state,t):
        x = state[0:self.n]
        y = state[self.n:2*self.n]# unpack the state vecto
        xdot = np.multiply(x,np.multiply(self.a-x,x-np.ones(self.n)))-y+self.k*(np.matmul(self.A,x)-(self.n-1)*x) # Global coupling only
        y = np.multiply(self.b,x)-np.multiply(self.c,y)
        state[0:self.n] = xdot
        state[self.n:2*self.n] = y
        return state

    def interpolateCurve(self):
        if self.states is None:
            self.states()
        values = np.array(self.states).transpose()
        s = []
        lastPoint = values[:,0]
        lastS = 0
        for i, point in enumerate(values[0]):
            point = values[:,i]
            lastS = math.sqrt(np.dot(np.array(point-lastPoint),np.array(point-lastPoint)))+lastS
            s.append(lastS)
            lastPoint = point
        s2 = np.linspace(s[0],s[-1],len(s))
        interpedData = []
        for dim in range(0,len(values[:,0])):
            data = np.array(values[dim,:]).reshape(len(s),1).squeeze()
            dimData = []
            s2Index = 0
            lastIndex = 0
            for i, value in enumerate(data):
                if i % 5 == 0 and i+5 <= len(s):
                    if i+5 == len(s):
                        tck, u = spl(np.array(data[i-2:i+4]).reshape(1,6),u = np.array(s[i-2:i+4]).reshape(6,1).flatten(),k = 5)
                        newValues = splev(s2[lastIndex:-1],tck)
                        for xi in newValues:
                            for xij in xi:
                                dimData.append(xij)
                    else:
                        tck, u = spl(np.array(data[i:i+6]).reshape(1,6),u = np.array(s[i:i+6]).reshape(6,1).flatten(),k = 5)
                        while s2[s2Index] < s[i+5]:
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
