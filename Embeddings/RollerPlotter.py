import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
import matplotlib.cm as cm
from os import listdir
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import NullFormatter
from sklearn import datasets



files = listdir('./SwissRoll/')
print(files)
roll = np.loadtxt('./DataSets/SwissRollData.txt')
col = np.loadtxt('./DataSets/SRcolor.txt')

#Make color maps
colmap = cm.get_cmap('plasma')

################################ Plot original datasets #################################
# fig = plt.figure()
# axlor = plt.subplot(121,projection = '3d')
# axros = plt.subplot(122,projection = '3d')
# # Rossler plot
# axros.plot(rossler[:,0],rossler[:,1],rossler[:,2],linewidth=0.7,alpha = 0.8)
# # Rossler plot
# axlor.plot(lorentz[:,0],lorentz[:,1],lorentz[:,2],linewidth=0.7,alpha = 0.8)
# plt.show()

################################# Plot with Color ######################################
fig = plt.figure()
ax = fig.add_subplot(241,projection = '3d')
ax.scatter(roll[:, 0], roll[:, 1], roll[:, 2], c=col, cmap=colmap,s = 75 )
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

#ax.set_yticklabels([])
#ax.set_xticklabels([])
#ax.set_zticklabels([])
plt.title('Original Swiss Roll')
plt.axis('tight')
titles = ['Isomap','Hessian LLE','LTSA','modified LLE', 'Standard LLE', 'PCA','TSNE']
for i,file in enumerate(files):
    emb = np.loadtxt('./SwissRoll/'+file)
    ax = fig.add_subplot(242+i)
    ax.scatter(emb[:,0],emb[:,1],c=col,cmap=colmap, s =75)
    #ax.xaxis.set_major_formatter(NullFormatter())
    #ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')
    plt.title('Embedded dataset using '+titles[i])

plt.show()

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
