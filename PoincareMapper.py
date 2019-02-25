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
    def __init__(self,plane,array):
        self.array = array
        self.plane = plane
        # Genarilze to more dimensions
        u1 = np.array([-plane[1],1,0])
        v2 = np.array([-plane[2],0,1])
        e1 = np.linalg.norm(u1)*u1
        u2 = v2 - np.dot(u1,v2)/np.dot(u1,u1)*u1
        e2 = np.linalg.norm(u2)*u2
        self.matrix = np.array([e1,e2])

    #Decide if 2 points are crossing
    def crossing(self,x1,x2):
        return np.dot(x1,self.plane)*np.dot(x2,self.plane)<0

    # distance to plane of a point
    def disPlan(self,x):
        return np.dot(x,self.plane)

    # Maps points interpolated from the data
    def map(self):
        values = []
        #Specify direction
        direction = 1
        # 2 to minus 4 for interpolation
        for i in range(2,len(self.array)-4):
            x1 = self.array[i]
            x2 = self.array[i+1]
            if(self.crossing(x1,x2) and (np.dot(self.plane,x1)*direction > 0)):
                #Interpolate nearest point
                nearestPoint = self.interpolate(self.array[i-2:i+4])
                #Add to values
                values.append(nearestPoint)
        fig = plt.figure()
        ax = fig.gca(projection ='3d')
        x = np.array(values).transpose()
        ax.plot(self.array[0],self.array[1],self.array[2],'o',linewidth=0.5,alpha = 0.9)
        ax.plot(x[0],x[1],x[2],'or',linewidth=0.5,alpha = 0.9)
        plt.show()
        return np.asarray(values)

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
        # two approaches one iterating over the expected values, and one
        curve = splev(np.linspace(0,1,1000),tck)
        curve = np.array(curve).transpose()
        min = self.disPlan(curve[0])
        for point in curve:
            tmp = self.disPlan(point)
            if(min>self.disPlan(point)):
                min = tmp
        return point
