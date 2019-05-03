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


newData = False

if newData:
    fitz = FitzSimulator()
    print('Simulating system')
    data = fitz.states(duration = 200000, split = 0.1, rtol = 1.49012e-9, atol = 1.49012e-9)
    print('Interpolating curve')
    data = fitz.interpolateCurve()[1000:]

    np.savetxt('DataFitz.txt',data)
else:
    data = np.loadtxt('DataFitz.txt')
    # poincareSection = np.loadtxt('Fitz4DPoincare.txt')
    # extremeEvents = np.array([i for i, point in enumerate(poincareSection) if(point[2]>=0.1)])
    # manifoldOfPoincareSection = np.loadtxt('Fitz4DManifold.txt')

# normalVector = np.array([0,0,1/math.sqrt(2),1/math.sqrt(2)]) # Includes extreme events
normalVector = np.array([1/math.sqrt(2),1/math.sqrt(2),0,0]) # Orthogonal to extreme events
# normalVector = np.array([0,0,1,0])

print('Constructing Poincare section')
mapper = PoincareMapper(normalVector,data)
poincareSection = np.array(mapper.getValues())
interindxes = mapper.getIntersctIndx()
np.savetxt('Fitz4DPoincare.txt',poincareSection)


poincareSection2 = np.array([point for point in poincareSection if(point[2]<0.1)])
extremeEvents = np.array([i for i, point in enumerate(poincareSection) if(point[2]>=0.1)])
index = np.array([i for i, point in enumerate(poincareSection) if(point[2]<0.1)])

print('Number of extreme events = %g' % len(extremeEvents))

print("Computing LLE embedding of return map")
# manifoldOfPoincareSection, err = manifold.Isomap(8,2).fit_transform(poincareSection) # return map then manifold
# print("Done. Reconstruction error: %g" % err)
manifoldOfPoincareSection = manifold.Isomap(12,2).fit_transform(poincareSection) # return map then manifold
np.savetxt('Fitz4DManifoldIso12.txt',manifoldOfPoincareSection)


## Fix colors for Plot
red = colors.to_rgba('red')
col = cm.get_cmap('plasma')
normdata = [np.linalg.norm(point) if(point[2]<0.1) else 0 for point in poincareSection]
normalize = colors.Normalize(vmin=0, vmax=max(normdata))
poincColor = [col(normalize(value)) if(value != 0) else red for value in normdata]

print('Plotting data')
fig = plt.figure()

ax = fig.add_subplot(221)
ax.set_title('Oscillator 1')
ax.plot(data[:,0],data[:,2], alpha = 0.5)
ax.scatter(poincareSection[:,0],poincareSection[:,2],c = poincColor, alpha = 0.8)

ax = fig.add_subplot(222)
ax.set_title('Oscillator 2')
ax.plot(data[:,1],data[:,3], alpha = 0.5)
ax.scatter(poincareSection[:,1],poincareSection[:,3],c = poincColor, alpha = 0.8)

ax = fig.add_subplot(223)
ax.set_title('Reembedded Poincaré Section')
ax.scatter(manifoldOfPoincareSection[:,0],manifoldOfPoincareSection[:,1],c = poincColor)
#ax.scatter(manifoldOfPoincareSection[extremeEvents-1,0],manifoldOfPoincareSection[extremeEvents-1,1],c = 'black')

ax = fig.add_subplot(224)
ax.set_title('Return map of reembedded Poincaré section')
ax.scatter(manifoldOfPoincareSection[:-1,1],manifoldOfPoincareSection[1:,1],c = poincColor[:-1], s = 5)
# ax.scatter(manifoldOfPoincareSection[extremeEvents-1,0],manifoldOfPoincareSection[extremeEvents,0], c = 'black')


plt.show()
