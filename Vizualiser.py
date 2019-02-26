from Simulator import Simulator
from PoincareMapper import PoincareMapper
import matplotlib.pyplot as plt
import numpy as np

class Vizualiser:
    def __init__(self,simulator,poincareMapper):
        self.poincareMapper = poincareMapper
        self.simulator = simulator
        self.data = simulator.getData()
        self.intersect = poincareMapper.getValues()

    def simplePlot(self,dim = [0,1,2]):
        sol = self.data
        intersect = np.array(self.intersect).transpose()
        # First plot of figure and points
        fig = plt.figure(figsize=plt.figaspect(0.5))
        ax = fig.add_subplot(1, 2, 1, projection='3d')
        ax.plot(sol[dim[0]],sol[dim[1]],sol[dim[2]],linewidth=0.5,alpha = 0.9 )
        ax.plot(intersect[dim[0]],intersect[dim[1]],intersect[dim[2]],'or',markersize=1,alpha = 0.4 )
        plt.title('Plot of differential points intersecting poincaré plane')

        #Second plot of poincare planeself.
        ax = fig.add_subplot(1, 2, 2)
        plane = self.poincareMapper.planePoints()
        ax.plot(plane[0],plane[2],'or',markersize =3)
        plt.title('The points on plane')


        plt.show()

    def z1Toz2Plot(self,dim = [0,1,2]):
        sol = self.data
        intersect = np.array(self.intersect).transpose()
        # First plot of figure and points
        fig = plt.figure(figsize=plt.figaspect(0.5))
        ax = fig.add_subplot(1, 2, 1, projection='3d')
        ax.plot(sol[dim[0]],sol[dim[1]],sol[dim[2]],linewidth=0.5,alpha = 0.9 )
        ax.plot(intersect[dim[0]],intersect[dim[1]],intersect[dim[2]],'or',markersize=1,alpha = 0.4 )

        #Second plot of poincare planeself.
        ax = fig.add_subplot(1, 2, 2)
        z = self.poincareMapper.iterationdifference()
        ax.plot(z[0],z[1],'or',markersize =3)


        plt.show()
