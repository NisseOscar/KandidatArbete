import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.animation as animation
from matplotlib.ticker import NullFormatter

manifold = np.loadtxt('Fitz4DManifold.txt')

rMap = np.array([[manifold[i,0],manifold[i+1,0]] for i in range(0,len(manifold)-1)])

arr0 = manifold[:,0]
axis = 0

def maxfunc(arr):
    return np.argmax(arr,axis = 1)

def recrsiveClosest(arr,strtP,dir,notInlcd,incld):
    notInclcd = notInclcd + [p for p in arr if(strtP[axis] > dir*strtP[axis])]
    inclcd = inclcd + [p for p in arr if(strtP[axis] <= dir*strtP[axis])]
    arr = [p for p in arr if(strtP[axis] < dir*strtP[axis])]
    if not arr:
        return incld,notInlcd
    else:
        distBtwn = [np.linalg.norm(strt-p) for p in arr]
        minindx = min(distBtwn)
        return  recrsiveClosest(arr,arr[minindx],dir,notInlcd,incld)

def separator(arr):
    maxIndx = maxfunc(np.array(arr)[:,0])
    print(maxIndx)
    maxi = arr[maxIndx]
    print(maxi)
    left = [p for p in arr if(p[axis]<maxi[axis])]
    right = [p for p in arr if(p[axis]>=maxi[axis])]
    chainL, overl = recrsiveClosest(leftm,maxi,1,[],[])
    chainr, overr = recrsiveClosest(right,maxi,-1,[],[])
    chain = chainL+ chainr
    leftover + overl+overr
    if(len(chain)+1 == len(arr)):
        return chain
    else:
        return chain + separator()

separated = separator(rMap)
