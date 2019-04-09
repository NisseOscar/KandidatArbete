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
import matplotlib.cm as cm
import matplotlib.colors as colors


newData = True

if newData:
    fitz = FitzSimulator()
    print('Simulating system')
    data = fitz.states(duration = 200000, split = 0.1, rtol = 1.49012e-9, atol = 1.49012e-9)
    print('Interpolating curve')
    data = fitz.interpolateCurve()[1000:]

    np.savetxt('DataFitz.txt',data)
else:
    data = np.loadtxt('DataFitz.txt')

# normalVector = np.array([0,0,1/math.sqrt(2),1/math.sqrt(2)]) # Includes extreme events
normalVector = np.array([1/math.sqrt(2),1/math.sqrt(2),0,0]) # Orthogonal to extreme events
# normalVector = np.array([0,0,1,0])

print('Constructing Poincare section')
mapper = PoincareMapper(normalVector,data)
poincareSection = np.array(mapper.getValues())
interindxes = mapper.getIntersctIndx()


poincareSection2 = np.array([point for point in poincareSection if(point[2]<0.1)])

extremeEvents = []
index = []
for i,point in enumerate(poincareSection):
    if point[2] > 0.1:
        extremeEvents.append(i)
    else:
        index.append(i)
extremeEvents = np.array(extremeEvents)
print('Number of extreme events = %g' % len(extremeEvents))

print("Computing LLE embedding of return map")
manifoldOfPoincareSection, err = manifold.locally_linear_embedding(poincareSection2,n_neighbors=8,n_components=2,method = 'modified') # return map then manifold
print("Done. Reconstruction error: %g" % err)

## Fix colors for Plot
col = col = cm.get_cmap('plasma')
normdata = [np.linalg.norm(point) for point in poincareSection2]
normalize = colors.Normalize(vmin=min(normdata), vmax=max(normdata))
dataColors = [col(normalize(value)) for value in normdata]
poincColor = [dataColors[i] for i in range(0,len(poincareSection2))]

print('Plotting data')
fig = plt.figure()

ax = fig.add_subplot(221)
ax.set_title('Oscillator 1')
ax.plot(data[:,0],data[:,2], alpha = 0.5)
ax.scatter(poincareSection2[:,0],poincareSection2[:,2],c = poincColor, alpha = 0.8)

ax = fig.add_subplot(222)
ax.set_title('Oscillator 2')
ax.plot(data[:,1],data[:,3], alpha = 0.5)
ax.scatter(poincareSection2[:,1],poincareSection2[:,3],c = poincColor, alpha = 0.8)

ax = fig.add_subplot(223)
ax.set_title('Reembedded Poincaré Section')
ax.scatter(manifoldOfPoincareSection[:,0],manifoldOfPoincareSection[:,1],c = poincColor)
ax.scatter(manifoldOfPoincareSection[extremeEvents-1,0],manifoldOfPoincareSection[extremeEvents-1,1],c = 'r')

ax = fig.add_subplot(224)
ax.set_title('Return map of reembedded Poincaré section')
ax.scatter(manifoldOfPoincareSection[:-1,0],manifoldOfPoincareSection[1:,0],c = poincColor[1:], s = 5)
ax.scatter(manifoldOfPoincareSection[extremeEvents,0],manifoldOfPoincareSection[extremeEvents+1,0], c = 'r')


plt.show()
