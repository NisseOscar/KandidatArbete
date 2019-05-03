import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.animation as animation
from matplotlib.ticker import NullFormatter



print('loading data')
data = np.loadtxt('./FitzFilesO/DataFitz.txt')
poincareSection = np.loadtxt('./FitzFilesO/Fitz4DPoincare.txt')
extremeEvents = np.array([i for i, point in enumerate(poincareSection) if(point[2]>=0.1)])
manifoldOfPoincareSection = np.loadtxt('./FitzFilesO/Fitz4DManifold.txt')


## Fix colors for Plot
print('Coloring')
red = colors.to_rgba('red')
col = cm.get_cmap('plasma')
normdata = [np.linalg.norm(point) if(point[2]<0.1) else 0 for point in poincareSection]
normalize = colors.Normalize(vmin=0, vmax=max(normdata))
poincColor = [col(normalize(value)) if(value != 0) else red for value in normdata]

print('Initate figure')
fig = plt.figure()
ax = fig.add_subplot(111)
#ax.scatter(manifoldOfPoincareSection[:,0],manifoldOfPoincareSection[:,1],c = poincColor)
ax.scatter(manifoldOfPoincareSection[:-1,0],manifoldOfPoincareSection[1:,0],c = poincColor[:-1], s = 5)
ax.yaxis.set_major_formatter(NullFormatter())
ax.xaxis.set_major_formatter(NullFormatter())
axExtrm = ax.twinx()
axExtrm.yaxis.set_major_formatter(NullFormatter())
axExtrm.xaxis.set_major_formatter(NullFormatter())

print('Animate')
def animate(i):
    axExtrm.clear()
    axExtrm.yaxis.set_major_formatter(NullFormatter())
    axExtrm.xaxis.set_major_formatter(NullFormatter())
    axExtrm.set_xlim(ax.get_xlim())
    axExtrm.set_ylim(ax.get_ylim())
    #axExtrm.scatter(manifoldOfPoincareSection[extremeEvents-i,0],manifoldOfPoincareSection[extremeEvents-i,1],c = 'black')
    axExtrm.scatter(manifoldOfPoincareSection[extremeEvents-1-i,0],manifoldOfPoincareSection[extremeEvents-i,0], c = 'black')

ani = animation.FuncAnimation(
    fig, animate,8, interval=1000, blit=False, save_count=50)

plt.show()
