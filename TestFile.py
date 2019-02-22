import Equation
from Simulator import Simulator
from PoincareMapper import PoincareMapper
import matplotlib.pyplot as plt
import numpy as np
import math


eq = Equation.Lorentz()
sim = Simulator(eq,init = eq.inCond())
newData = True
# newData = False
if newData:
    state = sim.states(100,0.01)
    sim.storeData('TestDataLorenz')
    states = sim.states.y
else:
    sim.loadData('TestDataLorenz')
    states = sim.states




# x,y = np.meshgrid(np.linspace(min(states[:,0]),max(states[:,0])),np.linspace(min(states[:,1]),max(states[:,1])))
planeVector = np.array([1,0,1])



# plt.figure(1)

mapper = PoincareMapper(planeVector,states,sim.t)
values = mapper.map2()

print(states.shape)
# plt.plot(values[1,0:len(values)-1],values[1,1:len(values)],'.')

fig = plt.figure(2)
ax = fig.gca(projection ='3d')
ax.plot(states[0,:], states[1,:], states[2,:],alpha = 0.8)

# if planeVector[2] == 0:
    # z = 0 # TODO solve how to calculate the plane
# else:
    # planeVector = planeVector/math.sqrt(planeVector.dot(planeVector))
    # z = (-planeVector[0]*x-planeVector[1]*y)/planeVector[2]

#ax.plot_surface(x,y,z,alpha = 0.4)
#plt.plot(states[:,0], states[:,1], states[:,2])

plt.show()
