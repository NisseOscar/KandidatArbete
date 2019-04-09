import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn import manifold, datasets
from Simulator import Simulator
from PoincareMapper import PoincareMapper
import Equation
import math
from scipy.integrate import odeint
from FitzSimulator import FitzSimulator


newData = True

if newData:
    fitz = FitzSimulator()
    print('Simulating system')
    data = fitz.states(duration = 50000, split = 0.1, rtol = 1.49012e-9, atol = 1.49012e-9)
    print('Interpolating curve')
    data = fitz.interpolateCurve()[1000:]

    normalVector = np.array([1/math.sqrt(2),0,1/math.sqrt(2),0]) # Includes extreme events
    # normalVector = np.array([0,1/math.sqrt(2),0,1/math.sqrt(2)]) # Orthogonal to extreme events

    mapper = PoincareMapper(normalVector,data)
    poincareSection = mapper.getValues()

    for point in poincareSection:
        if 

    print("Computing LLE embedding of return map")
    manifoldOfPoincareSection, err = manifold.locally_linear_embedding(poincareSection,n_neighbors=8,n_components=2,method = 'modified') # return map then manifold
    print("Done. Reconstruction error: %g" % err)

    np.savetxt('DataFitz.txt',data)
    np.savetxt('ManifoldPoincareFitz.txt',manifoldOfPoincareSection)
else:
    data = np.loadtxt('DataFitz.txt')
    manifoldOfPoincareSection = np.loadtxt('ManifoldOfPoincareFitz.txt')


fig = plt.figure()

ax = fig.add_subplot(131)
ax.set_title('Oscillator 1')
ax.plot(data[:,0],data[:,2])

ax = fig.add_subplot(132)
ax.set_title('Oscillator 2')
ax.plot(data[:,1],data[:,3])

ax = fig.add_subplot(133)
ax.set_title('Reembedded Poincaré Section')
ax.scatter(manifoldOfPoincareSection[:,0],manifoldOfPoincareSection[:,1])

plt.show()
