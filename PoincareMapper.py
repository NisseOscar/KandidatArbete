import numpy as np
from math import sin
import math
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
from scipy import signal
from scipy.optimize import newton

class PoincareMapper:
    def __init__(self,plane,array,t):
        self.array = array
        self.plane = plane
        self.t = t
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

    def map(self): # Maps points interpolated from the data
        values = []
        direction = 1
        for i in range(len(self.array)-1):
            x1 = self.array[i]
            x2 = self.array[i+1]
            if(self.crossing(x1,x2)) and (np.dot(self.plane,x1)*direction > 0):
                nearestPoint = self.projection(x1,x2)
                values.append(self.matrix.dot(nearestPoint))
        return np.asarray(values)

    def fourthOrderInterpolation(self,points, t, normalVector, nCrossing):
        # points is a matrix with the points represented as column vectors
        # nCrossing is wich point precedes the nCrossing

        # Create polynomial
        T = np.array([[pow(t[0],4), pow(t[0],3), pow(t[0],2), t[0], 1],\
        [pow(t[1],4), pow(t[1],3), pow(t[1],2), t[1], 1],\
        [pow(t[2],4), pow(t[2],3), pow(t[2],2), t[2], 1],\
        [pow(t[3],4), pow(t[3],3), pow(t[3],2), t[3], 1],\
        [pow(t[4],4), pow(t[4],3), pow(t[4],2), t[4], 1]])

        A = np.dot(np.linalg.inv(T),points)

        print('[T] = '+str(T.shape))
        print('[A] = ' +str(A.shape))
        print('[points] = ' + str(points.shape))

        def distToPlane(time):
            return np.dot(normalVector,np.dot(np.array([math.pow(time,4), math.pow(time,3), math.pow(time,2), time, 1]),A))

        # Initial conditions
        t0 = t[nCrossing]+(t[nCrossing+1]-t[nCrossing])*abs(np.dot(normalVector,points[nCrossing,:]))/abs(np.dot(normalVector,points[nCrossing,:]-points[nCrossing+1,:]))

        # Newton-Raphsons
        t1 = newton(distToPlane,t0,maxiter=10000) # PROBLEM WITH CONVERGENCE

        # Return intersection
        print('return '+str(np.dot(np.transpose(A),np.array([math.pow(t1,4), math.pow(t1,3), math.pow(t1,2), t1, 1]))))
        return np.dot(np.transpose(A),np.array([math.pow(t1,4), math.pow(t1,3), math.pow(t1,2), t1, 1]))


    def interp4thorder(self,points,t,normalVector,nCrossing):
        coeff = np.polyfit(t,points)
        def distToPlane(time):
            return np.dot(normalVector,np.dot())



    def map2(self):
        values = []
        direction = 1
        for i in range(len(self.array)-1):
            x1 = self.array[i]
            x2 = self.array[i+1]
            if(self.crossing(x1,x2)) and (np.dot(self.plane,x1)*direction > 0):
                #nearestPoint = self.projection(x1,x2)
                points = []
                tOfPoints = []
                nCrossing = 0
                # Choose the fifth point (assumes a fairly even distibution of points)
                if np.dot(self.plane,self.array[i-2])<np.dot(self.plane,self.array[i+3]):
                    points = np.array([self.array[i-2], self.array[i-1], self.array[i], self.array[i+1], self.array[i+2]])
                    tOfPoints = np.array([self.t[i-2], self.t[i-1], self.t[i], self.t[i+1], self.t[i+2]])
                    nCrossing = 3
                else:
                    points = np.array([self.array[i-1], self.array[i], self.array[i+1], self.array[i+2], self.array[i+3]])
                    tOfPoints = np.array([self.t[i-1], self.t[i], self.t[i+1], self.t[i+2], self.t[i+3]])
                    nCrossing = 2
                values.append(self.fourthOrderInterpolation(points,tOfPoints,self.plane,nCrossing))
        return np.asarray(values)
