import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.animation as animation
from matplotlib.ticker import NullFormatter
import math
import json




print('loading data')
data = np.loadtxt('DataFitz.txt')
poincareSection = np.loadtxt('Fitz4DPoincare.txt')
extremeEvents = np.array([i for i, point in enumerate(poincareSection) if(np.linalg.norm(point)>=0.1)])
manifoldOfPoincareSection = np.loadtxt('Fitz4DManifold.txt')

print('Generate containers')
y = manifoldOfPoincareSection[:,0]
rmap = np.array([y[:-1],y[1:]])
maxi = max(y)
mini = min(y)
mid = rmap[0,np.argmax(rmap,axis=1)][1]

print('Creating segments')
seg = 5
segmentsl = np.linspace(mini,mid,seg)
segmentsr = np.linspace(mid,maxi,seg)
segments = np.concatenate((segmentsl,segmentsr[1:]))

totsequenze = [sum(p<segments) for p in y]
print(totsequenze)
print('Count extreme segments')
extrmsequze = []
freq = {}
for i in extremeEvents:
    previus = [y[i-j] for j in range(0,5)]
    sections = [sum(p<segments) for p in previus]
    sqnz =  0
    for i,p in enumerate(previus):
        sqnz = [sqnz + sum(p<segments)*math.pow(10,i)]
    if (sqnz in freq):
        freq[sqnz] += 1
    else:
        freq[sqnz] = 1

# for key in freq:



for key, value in freq.items():
        print ("% d : % d"%(key, value))
