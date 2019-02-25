from abc import ABC, abstractmethod
import numpy as np

class function(ABC):
    @abstractmethod
    def f(self,t,state):
        pass


class Lorentz(function):

    def __init__(self,values = [26.0,10.0,8.0/3.0]):
        self.rho = values[0]
        self.sigma = values[1]
        self.beta = values[2]

    def f(self,t,state):
        x,y,z = state
        return self.sigma * (y - x), x * (self.rho - z) - y, x * y - self.beta * z  # derivatives

    def inCond(self):
        return [1.0,1.0,1.0]

    def jacobian(self,state,t):
        return [[-self.sigma, self.sigma, 0],[self.rho-state[2], -1, -state[0]],[state[1], state[0], -self.beta]]


class Rossler(function):
    def __init__(self,values = [0.1,0.1,14.0]):
        self.a = values[0]
        self.b = values[1]
        self.c = values[2]

    def f(self,t,state):
      x, y, z = state  # unpack the state vector
      return -y-z, x+self.a*y,self.b+z*(x-self.c) # derivatives

    def inCond(self):
        return [1.0,1.0,1.0]
    def jacobian(self,state,t):
        return

class Fitz(function):
    def __init__(self,n=2,a = -0.02651,c=0.02,b = None,A = None,k=0.00128):
        self.n = n
        self.k = k
        if(isinstance(a,float)):
            self.a = a*np.ones(n)
        else:
            self.a = a
        if(isinstance(c,float)):
            self.c = c*np.ones(n)
        else:
            self.c = c
        if(A is None):
            self.A = 1-np.identity(n)
        if(b is None):
            self.b = np.linspace(0.0065,0.0135,n)

    def f(self,t,state):
      x = state[0:self.n]
      y = state[self.n:2*self.n]# unpack the state vector
      x = x*(self.a-x)*(x-1)-y+self.k*np.matmul(np.transpose(self.A)-self.A,x)
      y = self.b*x-self.c*y
      state[0:self.n] = x
      state[self.n:2*self.n] = y# unpack the state vector
      return state

    def inCond(self):
        return [1.0,1.0,1.0,1.0]
