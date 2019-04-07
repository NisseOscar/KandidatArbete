import numpy as np
from sklearn import manifold, datasets
#from ../colorPlot import ColorPlot
import math
import numpy as np

lorentz = np.loadtxt('LorentzData.txt')
rossler = np.loadtxt('RosslerData.txt')
print('loaded data')
methods = ['standard', 'ltsa']
data = {}
for method in methods:
    print('Constructing embedding of Rossler')
    rossEmb = manifold.LocallyLinearEmbedding(n_neighbors = 15, n_components=2,method = method,eigen_solver='auto').fit_transform(rossler)
    print('Constructing embedding of Lorentz')
    lorEmb = manifold.LocallyLinearEmbedding(n_neighbors = 15, n_components=2,method = method,eigen_solver='auto').fit_transform(lorentz)
    emb = [rossEmb,lorEmb]
    data[method] = emb

print('Doing Tsne embedding')
tsneRoss = manifold.TSNE(n_components=2, init='pca', random_state=0).fit_transform(rossler)
tsneLor =  manifold.TSNE(n_components=2, init='pca', random_state=0).fit_transform(lorentz)
data['TSNE'] = [tsneRoss,tsneLor]

print('Doing MDS embedding')
mdsRoss =  manifold.MDS(2, max_iter=100, n_init=1).fit_transform(rossler)
mdsLor =   manifold.MDS(2, max_iter=100, n_init=1).fit_transform(lorentz)
data['MDS'] = [mdsRoss,mdsLor]

print('Doing Isomap embedding')
isoRoss =  manifold.Isomap(15,2).fit_transform(rossler)
isoLor =   manifold.Isomap(15,2).fit_transform(lorentz)
data['Isomap'] = [isoRoss,isoLor]

print('Saving embeddings')
for emb in data:
    embData = data[emb]
    ross = embData[0]
    lor = embData[1]
    np.savetxt(emb+'Lorentz.txt', lor)
    np.savetxt(emb+'Rossler.txt', ross)
