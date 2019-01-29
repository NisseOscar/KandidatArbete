import numpy as np
from math import sin
import math
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
from scipy import signal


# Define the Rossler attractor

a = 0.2
b = 0.2
c = 5.7

def rossler(state,t):
    x,y,z = state
    return - y - z, x + a * y , b + z * ( x - c )



# These points define the plane used for the Poincare section
# https://en.wikipedia.org/wiki/Plane_(geometry)

p1 = np.array([0.0,0.0,0.0])
p2 = np.array([0.0,1.0,0.0])
p3 = np.array([0.0,0.0,1.0])

# Calculating the normal of the plane

normalVector = np.cross(p3-p1,p2-p1);


state0 = [1.0,1.0,1.0]
t = np.arange(0.0, 400.0, 0.01)
states = odeint(rossler, state0, t)

# Calculating the distance between each point and the plane, including the sign
# https://mathinsight.org/distance_point_plane


distance = np.array(np.prod([normalVector,states],axis = 0))


# Find points before intersection

dir = 1 # positive or negative
points = np.empty((int(np.ceil(len(distance))),1))
indeces = points

def crossing(point1,point2,direction):
    # Function returning true if the following point is on the other side of the plane and its in the right direction
    # Along the normal is positive direction and against is negative, %%%%%% check so that this is true %%%%%%
    if (point1*point2<0) and (point2*direction>0):
        return True
    else:
        return False
k = 0

# TODO change so that the exact intersection is calculated
for i in range(0,len(distance)-1):
    if crossing(distance[i,0],distance[i+1,0],dir):
        points[k] = t[i]
        indeces[k] = i
        k += 1


indeces = indeces.ravel()
points = points.ravel()

points = np.array(points[0:k])
indeces = np.array(indeces[0:k])
indeces = indeces.astype(int)



Yn = states[indeces[0:k-1],1]
YnPlus1 = states[indeces[1:k],1]

plt.plot(Yn,YnPlus1,'o')
plt.show()

# remove the #'s to plot distance and intersections in the given direction

#zeros = np.zeros((len(points),1))
#plt.plot(t,distance,'b',points,zeros,'ro')
#plt.show()
