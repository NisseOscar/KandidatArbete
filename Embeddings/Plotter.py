import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
import matplotlib.cm as cm
from os import listdir
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import NullFormatter

embFolder = 'RosslerEmbIntpltd'
files = listdir('./'+embFolder)

data = np.loadtxt('DataSets/RosslerInpltd.txt')

#Make color maps
colmap = cm.get_cmap('plasma')
#Rossler
rossnorm = colors.Normalize(vmin=min(data.T[2]), vmax=max(data.T[2]))
col = [colmap(rossnorm(value)) for value in data.T[2]]

################################ Plot original datasets #################################
# fig = plt.figure()
# axlor = plt.subplot(121,projection = '3d')
# axros = plt.subplot(122,projection = '3d')
# # Rossler plot
# axros.plot(rossler[:,0],rossler[:,1],rossler[:,2],linewidth=0.7,alpha = 0.8)
# # Rossler plot
# axlor.plot(lorentz[:,0],lorentz[:,1],lorentz[:,2],linewidth=0.7,alpha = 0.8)
# plt.show()
######################## Plot Dot color ###################################
fig = plt.figure()
ax = fig.add_subplot(241,projection = '3d')
ax.scatter(data[:, 0], data[:, 1], data[:, 2], c = col,s = 10,alpha=0.8 )
ax.set_yticklabels([])
ax.set_xticklabels([])
ax.set_zticklabels([])
plt.title('Simulated Rossler dataset with interpolation')
plt.axis('tight')
titles = ['Isomap','Hessian LLE','LTSA','modified LLE', 'Standard LLE', 'PCA','TSNE']
for i,file in enumerate(files):
    emb = np.loadtxt('./'+embFolder+'/'+file)
    ax = fig.add_subplot(242+i)
    ax.scatter(emb[:,0],emb[:,1],c = col, s =10,alpha=0.8)
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')
    plt.title('Embedded dataset using '+titles[i])

plt.show()
################################# Plot with Color ######################################
# seglen = 5
# for file in files:
#     lorentzemb = np.loadtxt('./datafiles/'+file[0])
#     rossleremb = np.loadtxt('./datafiles/'+file[1])
#     fig = plt.figure()
#     axlor = plt.subplot(121)
#     axros = plt.subplot(122)
#     for i in range(int((len(lorentzemb)-seglen)/seglen)):
#         # Rossler plot
#         embRoss = rossleremb[seglen*i:seglen*i+seglen]
#         axros.plot(embRoss[:,0],embRoss[:,1], color = rosscolors[int(seglen*i+seglen/2)],linewidth=0.7,alpha = 0.8)
#         # Rossler plot
#         embLor = rossleremb[seglen*i:seglen*i+seglen]
#         axlor.plot(embLor[:,0],embLor[:,1], color = lorcolors[int(seglen*i+seglen/2)],linewidth=0.7,alpha = 0.8)
#     plt.show()

########################### Plot without color #############################
# for file in files:
#     lorentzemb = np.loadtxt('./datafiles/'+file[0])
#     rossleremb = np.loadtxt('./datafiles/'+file[1])
#     fig = plt.figure()
#     fig.suptitle(file[0]+', '+file[1])
#     axlor = plt.subplot(121)
#     axlor.yaxis.set_major_formatter(NullFormatter())
#     axlor.xaxis.set_major_formatter(NullFormatter())
#     axros = plt.subplot(122)
#     axros.yaxis.set_major_formatter(NullFormatter())
#     axros.xaxis.set_major_formatter(NullFormatter())
#     axlor.plot(lorentzemb[:,0],lorentzemb[:,1],linewidth=0.7,alpha = 0.8)
#     axros.plot(rossleremb[:,0],rossleremb[:,1],linewidth=0.7,alpha = 0.8)
#
# plt.show()
