import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class ColorPlot:
    def __init__(self,simFile = 'simData.txt',manFile = 'manData.txt', seglen = 10, simData = [], manData = []):
        # Check types
        #if not (simFile is str & manFile is str & seglen is int):
        #    raise Exception('Wrong types')
        # Load simData and construct colormap on criteria of warmth
        if( manData == [] or simData == []):
            self.simData = np.loadtxt(simFile)
            self.manData = np.loadtxt(manFile)
        else:
            self.manData = manData
            self.simData = simData
        col = cm.get_cmap('coolwarm')
        normalize = colors.Normalize(vmin=min(self.simData[2]), vmax=max(self.simData[2]))
        self.colors = [col(normalize(value)) for value in self.simData[2]]
        # Load manifolddata.
        self.seglen = seglen

    # Plot the data according to the colorschema where ax could be a predifined axis or not.
    # ax being the axis to operate on
    # plot is a boolean if it should plot the figure or not
    def plotMan(self,ax = None,plot = False):
        if(ax == None):
            fig = plt.figure()
            ax = plt.gca()
        # Setting segment length for simpler computation
        n = self.seglen
        # Plot each to the average color of the segment
        for i in range(int((len(self.manData)-n)/n)):
            tsneSegi = self.manData[n*i:n*i+n]
            ax.plot(tsneSegi[:,0],tsneSegi[:,1], color = self.colors[int(n*i+n/2)],linewidth=0.7,alpha = 0.8)
        if (plot):
            plt.show()

    # Plot the data according to the colorschema where ax could be a predifined axis or not.
    # ax being the axis to operate on
    # plot is a boolean if it should plot the figure or not
    def plotSim(self,ax = None,plot = False):
        if(ax == None):
            fig = plt.figure()
            ax = plt.gca(projection = '3d')
        # Setting segment length for simpler computation
        n = self.seglen
        simData = self.simData.T
        # Plot each to the average color of the segment
        for i in range(int((len(simData)-n)/n)):
            tsneSegi = simData[n*i:n*i+n]
            ax.plot(tsneSegi[:,0],tsneSegi[:,1],tsneSegi[:,2], color = self.colors[int(n*i+n/2)],linewidth=0.7,alpha = 0.8)
        if (plot):
            plt.show()
        return ax;

    def getColorMap(self):
        return self.colors
