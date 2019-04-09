import numpy as np
from sklearn import manifold, datasets
#from ../colorPlot import ColorPlot
import math
import numpy as np

lorentz = np.loadtxt('LorentzData.txt')
rossler = np.loadtxt('RosslerData.txt')
print('loaded data')
methods = ['standard', 'ltsa', 'hessian', 'modified']
for method in methods:
    print('Constructing embedding of Rossler')
    rossEmb = manifold.LocallyLinearEmbedding(n_neighbors = 10, n_components=2,method = method,eigen_solver='auto').fit_transform(rossler)
    print('Constructing embedding of Lorentz')
    lorEmb = manifold.LocallyLinearEmbedding(n_neighbors = 10, n_components=2,method = method,eigen_solver='dense').fit_transform(lorentz)
    np.savetxt('./datafiles/LLE'+method+'Lorentz.txt', lorEmb)
    np.savetxt('./datafiles/LLE'+method+'Rossler.txt', rossEmb)

print('Doing Tsne embedding')
print('Constructing embedding of Rossler')
rossEmb = manifold.TSNE(n_components=2, init='pca', random_state=0).fit_transform(rossler)
print('Constructing embedding of Lorentz')
lorEmb =  manifold.TSNE(n_components=2, init='pca', random_state=0).fit_transform(lorentz)
np.savetxt('./datafiles/TSNELorentz.txt', lorEmb)
np.savetxt('./datafiles/TSNERossler.txt', rossEmb)

print('Doing MDS embedding')
print('Constructing embedding of Rossler')
rossEmb =  manifold.MDS(2, max_iter=100, n_init=1).fit_transform(rossler)
print('Constructing embedding of Lorentz')
lorEmb =   manifold.MDS(2, max_iter=100, n_init=1).fit_transform(lorentz)
np.savetxt('./datafiles/MDSLorentz.txt', lorEmb)
np.savetxt('./datafiles/MDSRossler.txt', rossEmb)

print('Doing Isomap embedding')
print('Constructing embedding of Rossler')
rossEmb =  manifold.Isomap(12,2).fit_transform(rossler)
print('Constructing embedding of Lorentz')
lorEmb =   manifold.Isomap(12,2).fit_transform(lorentz)
np.savetxt('./datafiles/ISOLorentz.txt', lorEmb)
np.savetxt('./datafiles/ISORossler.txt', rossEmb)

print('Doing Spectral embedding')
print('Constructing embedding of Rossler')
rossEmb =  manifold.SpectralEmbedding(n_components=2,n_neighbors=12).fit_transform(rossler)
print('Constructing embedding of Lorentz')
lorEmb =   manifold.SpectralEmbedding(n_components=2,n_neighbors=1).fit_transform(lorentz)
np.savetxt('./datafiles/SpectralLorentz.txt', lorEmb)
np.savetxt('./datafiles/SpectralRossler.txt', rossEmb)
