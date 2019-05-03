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

print('generating data')
data = np.loadtxt('./FitzFilesO/DataFitz.txt')
normalVector = np.array([1/math.sqrt(2),1/math.sqrt(2),0,0])
print('Constructing Poincare section')
mapper = PoincareMapper(normalVector,data)
poincareSection = np.loadtxt('./FitzFilesO/Fitz4DPoincare.txt')
manData = np.loadtxt('./FitzFilesO/Fitz4DManifold.txt')

segmts = 10


print('Generate containers')
y = manData[:,0]
rmap = np.array([y[:-1],y[1:]])
maxi = max(y)
mini = min(y)
mid = rmap[0,np.argmax(rmap,axis=1)][1]

print('Creating segments')
seg = segmts/2
segmentsl = np.linspace(mini,mid,seg)
segmentsr = np.linspace(mid,maxi,seg)
segments = np.concatenate((segmentsl,segmentsr[1:]))
print(segments)

print('genereating colors')
cmap = cm.get_cmap('plasma')
rgba = [cmap(i) for i in np.linspace(0,1,segmts)]
colors = [rgba[sum(p<segments)] for p in y]
print(colors)


print('Plotting data')
fig = plt.figure()

ax = fig.add_subplot(221)
ax.set_title('Oscillator 1')
ax.plot(data[:,0],data[:,2], alpha = 0.2)
ax.scatter(poincareSection[:,0],poincareSection[:,2],c = colors, alpha = 0.9)

ax = fig.add_subplot(222)
ax.set_title('Oscillator 2')
ax.plot(data[:,1],data[:,3], alpha = 0.2)
ax.scatter(poincareSection[:,1],poincareSection[:,3],c = colors, alpha = 0.9)

ax = fig.add_subplot(223)
ax.set_title('Reembedded Poincaré Section')
ax.scatter(manData[:,0],manData[:,1],c = colors)
#ax.scatter(manifoldOfPoincareSection[extremeEvents-1,0],manifoldOfPoincareSection[extremeEvents-1,1],c = 'black')

ax = fig.add_subplot(224)
ax.set_title('Return map of reembedded Poincaré section')
ax.scatter(y[:-1],y[1:],c = colors[:-1], s = 5)
# ax.scatter(manifoldOfPoincareSection[extremeEvents-1,0],manifoldOfPoincareSection[extremeEvents,0], c = 'black')


plt.show()
