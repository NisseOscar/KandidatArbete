import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class ColorPlot:
    def __init__(self,simFile = 'simData.txt', seglen = 10, simData = [],c = 'coolwarm'):

        # Load simData and construct colormap on criteria of warmth
        if(simData == []):
            self.simData = np.loadtxt(simFile)
        else:
            self.simData = simData
        col = cm.get_cmap(c)
        normalize = colors.Normalize(vmin=min(self.simData[2]), vmax=max(self.simData[2]))
        self.colors = [col(normalize(value)) for value in self.simData[2]]
        # Load manifolddata.
        self.seglen = seglen

    def d2plot(self,data,ax = None,plot = False):
        if(ax == None):
            fig = plt.figure()
            ax = plt.plot()
        # Setting segment length for simpler computation
        n = self.seglen
        Data = self.simData.T
        # Plot each to the average color of the segment
        for i in range(int((len(Data)-n)/n)):
            tsneSegi = Data[n*i:n*i+n]
            ax.plot(tsneSegi[:,0],tsneSegi[:,1], color = self.colors[int(n*i+n/2)],linewidth=0.7,alpha = 0.8)
        if (plot):
            plt.show()
        return ax;

    # Plot the data according to the colorschema where ax could be a predifined axis or not.
    # ax being the axis to operate on
    # plot is a boolean if it should plot the figure or not
    def d3plot(self,data,ax = None,plot = False,):
        if(ax == None):
            fig = plt.figure()
            ax = plt.gca(projection = '3d')
        # Setting segment length for simpler computation
        n = self.seglen
        Data = self.simData.T
        # Plot each to the average color of the segment
        for i in range(int((len(Data)-n)/n)):
            tsneSegi = Data[n*i:n*i+n]
            ax.plot(tsneSegi[:,0],tsneSegi[:,1],tsneSegi[:,2], color = self.colors[int(n*i+n/2)],linewidth=0.7,alpha = 0.8)
        if (plot):
            plt.show()
        return ax;

    def getColorMap(self):
        return self.colors
