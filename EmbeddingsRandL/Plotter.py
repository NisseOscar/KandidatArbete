import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
import matplotlib.cm as cm
from os import listdir
from mpl_toolkits.mplot3d import Axes3D


files = listdir('.\datafiles')
files = [[files[2*i],files[2*i+1]] for i in range(0,int(len(files)/2))]
print(files)

lorentz = np.loadtxt('LorentzData.txt')
rossler = np.loadtxt('RosslerData.txt')


#Make color maps
col = cm.get_cmap('plasma')
#Lorentz
lornorm = colors.Normalize(vmin=min(lorentz.T[2]), vmax=max(lorentz.T[2]))
lorcolors = [col(lornorm(value)) for value in lorentz.T[2]]
#Rossler
rossnorm = colors.Normalize(vmin=min(rossler.T[2]), vmax=max(rossler.T[2]))
rosscolors = [col(lornorm(value)) for value in rossler.T[2]]

seglen = 5
# Plot original datasets
fig = plt.figure()
axlor = plt.subplot(121,projection = '3d')
axros = plt.subplot(122,projection = '3d')
for i in range(int((len(lorentz)-seglen)/seglen)):
    # Rossler plot
    embRoss = rossler[seglen*i:seglen*i+seglen]
    axros.plot(embRoss[:,0],embRoss[:,1],embRoss[:,2], color = rosscolors[int(seglen*i+seglen/2)],linewidth=0.7,alpha = 0.8)
    # Rossler plot
    embLor = lorentz[seglen*i:seglen*i+seglen]
    axlor.plot(embLor[:,0],embLor[:,1],embLor[:,2], color = lorcolors[int(seglen*i+seglen/2)],linewidth=0.7,alpha = 0.8)
plt.show()

# Plot each to the average color of the segment
seglen = 5
for file in files:
    lorentzemb = np.loadtxt('./datafiles/'+file[0])
    rossleremb = np.loadtxt('./datafiles/'+file[1])
    fig = plt.figure()
    axlor = plt.subplot(121)
    axros = plt.subplot(122)
    for i in range(int((len(lorentzemb)-seglen)/seglen)):
        # Rossler plot
        embRoss = rossleremb[seglen*i:seglen*i+seglen]
        axros.plot(embRoss[:,0],embRoss[:,1], color = rosscolors[int(seglen*i+seglen/2)],linewidth=0.7,alpha = 0.8)
        # Rossler plot
        embLor = rossleremb[seglen*i:seglen*i+seglen]
        axlor.plot(embLor[:,0],embLor[:,1], color = lorcolors[int(seglen*i+seglen/2)],linewidth=0.7,alpha = 0.8)
    plt.show()

########################### Plot without color #############################
for file in files:
    lorentzemb = np.loadtxt('./datafiles/'+file[0])
    rossleremb = np.loadtxt('./datafiles/'+file[1])
    fig = plt.figure()
    axlor = plt.subplot(121)
    axros = plt.subplot(122)
    axlor.plot()
