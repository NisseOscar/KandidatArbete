import numpy as np
from sklearn import manifold, datasets
#from ../colorPlot import ColorPlot
import math

print('Loading data')
data = np.loadtxt('./DataSets/Lorentz.txt')
folder = 'Lorentzemb'

methods = ['standard', 'ltsa', 'hessian', 'modified']
for method in methods:
    print('Constructing embedding')
    emb = manifold.LocallyLinearEmbedding(n_neighbors = 10, n_components=2,method = method,eigen_solver='auto').fit_transform(data)
    print('Saving')
    np.savetxt('./'+folder+'/LLE'+method+'Rossler.txt', emb)

print('Doing Tsne embedding')
emb = manifold.TSNE(n_components=2, init='pca', random_state=0).fit_transform(data)
np.savetxt('./'+folder+'/TSNERossler.txt', emb)

print('Doing MDS embedding')
emb =  manifold.MDS(2, max_iter=100, n_init=1).fit_transform(data)
np.savetxt('./'+folder+'/MDSRossler.txt', emb)

print('Doing Isomap embedding')
emb =   manifold.Isomap(12,2).fit_transform(data)
np.savetxt('./'+folder+'/ISORossler.txt', emb)
