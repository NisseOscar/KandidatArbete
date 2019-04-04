import numpy as np
import numpy.linalg as lin
import Equation
from colorPlot import ColorPlot
import matplotlib.pyplot as plt
import math
from collections import deque

simData = np.loadtxt('Data.txt').T
eq = Equation.Rossler()
equalibriums = eq.equalibriumpoints()
# Calculate the equalibrium being close to the orbit.
accSimData= sum(simData.T)
# Calculate which equalibrium the equations orbits around. Gets an array of points.
orderedEqua = [[equa,sum(np.absolute(accSimData-simData.size*equa))] for equa in equalibriums ]
orderedEqua.sort(key=lambda dist:dist[1])
orderedEqua = [equa[0] for equa in orderedEqua]
dim = np.size(simData,0)

# Inital matrix of the hyperplane
P = np.zeros((dim-1,dim))
# Index of dimensions taken into consideration
k = 0

for equa in orderedEqua[:-1]:
    if( k >= dim-1):
        break;
    jac = eq.jacobian(equa)
    lam, v = lin.eig(jac)
    realV= v[:,np.imag(lam)==0]
    for vec in realV.T:
        # This yields a warning since casted to reell vecot, but that is okey as itallready is reell
        P[k] = vec
        k = k+1
    # Calculate projection to the current plane, (we want deviant points)
    proj = [lin.norm(np.matmul(P.T,P)*v2) for v2 in simData.T]
    # Number of compared compared local points local maximum
    neighbors = 1000
    #Deque of this structure
    que = deque(proj[:neighbors])
    # Iterate over projections and find local maximum
    for i in range(math.floor(neighbors/2+1),(len(proj)-math.floor(neighbors/2)-1)):
        que.popleft()
        que.append(proj[i+math.floor(neighbors/2)])
        if(all([proj[i]>=p for p in que])):
            vec = simData.T[i]
            vec = vec-np.matmul(np.matmul(P.T,P),vec)
            #Make sure vector isn't in the plane.
            if(lin.norm(vec)>=0.1):
                vec = vec/lin.norm(vec)
                P[k] = vec.T
                k = k+1
            if(k == dim-1):
                break
#Find normal towards the plane
# print(np.cross(P[1],P[0]))
print(P)
