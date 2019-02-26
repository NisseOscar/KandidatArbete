import Equation
from Simulator import Simulator
from Vizualiser import Vizualiser
from PoincareMapper import PoincareMapper
import matplotlib.pyplot as plt
import numpy as np
import math


eq = Equation.Rossler()
sim = Simulator(eq)
data = sim.states(duration=600)
#sim.tredimplot()

mapper = PoincareMapper([1,-3.3,0],data)
viz = Vizualiser(sim,mapper)
viz.simplePlot()
#a = mapper.planePoints()
#print(a)
#plt.plot(a[0],a[1],'o')
#plt.show()
