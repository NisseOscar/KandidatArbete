import Equation
from Simulator import Simulator
from Vizualiser import Vizualiser
from PoincareMapper import PoincareMapper
import matplotlib.pyplot as plt
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D


eq = Equation.Rossler()
sim = Simulator(eq)
data = sim.states(duration=600)
#sim.tredimplot()

mapper = PoincareMapper([0.5,-1,0],data,direction = 1)
viz = Vizualiser(sim,mapper)

def f(vector):
    return vector[2]

viz.z1Toz2Plot(fun = f)
#a = mapper.planePoints()
#print(a)
#plt.plot(a[0],a[1],'o')
#plt.show()
