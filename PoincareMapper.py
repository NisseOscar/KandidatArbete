import numpy as np
from math import sin
import math
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
from scipy import signal
from scipy.optimize import newton
from scipy.interpolate import splprep as spl
from scipy.interpolate import splev

class PoincareMapper:
    # Initiate with plane normal and data array
    def __init__(self,plane,array, direction = 1):
        self.array = array
        # The normal of the plane, in case of 3 dimensions, goes through origo.
        self.plane = plane/np.linalg.norm(plane)
        vec = self.plane[np.newaxis, :]
        self.proMatrix = np.identity(len(plane))-np.matmul(vec.T,vec)
        # Specify direction of intersection
        self.direction = direction
        self.map()

    #Decide if 2 points are crossing
    def crossing(self,x1,x2):
        return np.dot(x1,self.plane)*np.dot(x2,self.plane)<0

    # distance to plane of a point
    def disPlan(self,x):
        return np.dot(x,self.plane)

    # Maps points interpolated from the data
    def map(self):
        self.values = []
        for i in range(2,len(self.array)-4):
            x1 = self.array[i]
            x2 = self.array[i+1]
            if(self.crossing(x1,x2) and (np.dot(self.plane,x1)*direction > 0)):
                #Interpolate nearest point
                nearestPoint = self.interpolate(self.array[i-2:i+4])
                #Add to values
                self.values.append(nearestPoint)
        fig = plt.figure()
        ax = fig.gca(projection ='3d')
        x = np.array(values).transpose()
        ax.plot(self.array[0],self.array[1],self.array[2],'o',linewidth=0.5,alpha = 0.9)
        ax.plot(x[0],x[1],x[2],'or',linewidth=0.5,alpha = 0.9)
        plt.show()
        return np.asarray(self.values)

    #Calculate which 5 points of the crossing that are the closest
    def closestPoints(self,points):
        return points
        if( self.disPlan(points[0])<self.disPlan(points[-1])):
            return points[0:-1]
        else:
            return points[1:]

    #Interpolate by the 5th order
    def interpolate(self, crossingPoints):
        points = self.closestPoints(crossingPoints)
        points = points.transpose()
        tck,u = spl(points,k=5)
        # From our splines we calculate the approximate vactor and iterate to the closest point.
        # Could be done through newton raphosdy, not sure.
        curve = splev(np.linspace(0,1,1000),tck)
        curve = np.array(curve).transpose()
        min = self.disPlan(curve[0])
        for point in curve:
            tmp = self.disPlan(point)
            if(min>self.disPlan(point)):
                min = tmp
        return point

    def getValues(self):
        return self.values.copy()

    def get planeProjection():
        self.values
