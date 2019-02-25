import Equation
from Simulator import Simulator
from PoincareMapper import PoincareMapper
import matplotlib.pyplot as plt
import numpy as np
import math


eq = Equation.Rossler()
sim = Simulator(eq)
data = sim.states(duration=600)
sim.tredimplot()

mapper = PoincareMapper([0,1,0],data)
mapper.map()
