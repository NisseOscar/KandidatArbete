import numpy as np
from sklearn import manifold, datasets
from PoincareMapper import PoincareMapper
import math
from FitzSimulator import FitzSimulator
import matplotlib.cm as cm
import matplotlib.colors as colors
import json

print('initating data')
data = np.loadtxt('./FitzFilesO/DataFitz.txt')
normalVector = np.array([1/math.sqrt(2),1/math.sqrt(2),0,0]) # Orthogonal to extreme events
freq = {}
freqTot = {}


    #print('right now in iteration: '+str(i))
    #for iteratiions in range(1000)
print('simulating data')
fitz = FitzSimulator(inCond = data[-1])
print('Simulating system')
data = fitz.states(duration = 200000, split = 0.1, rtol = 1.49012e-9, atol = 1.49012e-9)
print('Interpolating curve')
#data = fitz.interpolateCurve()

print('making poincare map')
mapper = PoincareMapper(normalVector,data)
poincareSection = np.array(mapper.getValues())
extremeEvents = np.array([i for i, point in enumerate(poincareSection) if(np.linalg.norm(point)>=0.12)])

print('manifolding')
manifoldOfPoincareSection = manifold.Isomap(12,2).fit_transform(poincareSection) # return map then manifold

y = manifoldOfPoincareSection[:,0]

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

print('Count extreme segments')
print(extremeEvents)
for i in extremeEvents:
    if(i>=10):
        previus = [y[i-10+j] for j in range(0,10)]
        #Put extra catogory here!
        sqnz = ''.join([str(sum(p<segments)) for p in previus])
        if( sqnz in freq):
            freq[sqnz] += 1
        else:
            freq[sqnz] = 1
print(freq)

print('Saving')
# Save total sequence
totsequenze = ''.join([str(sum(p<segments)) for p in y])
with open("totSeq.txt", "a") as text_file:
    text_file.write(totsequenze)
#Saving results
with open('extrmSeq.json', 'w') as fp:
    json.dump(freq, fp)
