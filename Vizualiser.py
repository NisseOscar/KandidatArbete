from Simulator import Simulator
from PoincareMapper import PoincareMapper
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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
        #Plot planeself

        ax.hold(True)
        ax.plot(sol[dim[0]],sol[dim[1]],sol[dim[2]],linewidth=0.5,alpha = 0.9 )
        ax.plot(intersect[dim[0]],intersect[dim[1]],intersect[dim[2]],'or',markersize=1,alpha = 0.4 )
        #plt.title('Plot of differential points intersecting poincaré plane')

        #Second plot of poincare planeself.
        ax = fig.add_subplot(1, 2, 2)
        plane = self.poincareMapper.planePoints()
        ax.plot(plane[0],plane[2],'or',markersize =3)
        #plt.title('The points on plane')


        plt.show()

    def z1Toz2Plot(self,dim = [0,1,2],fun = np.linalg.norm):
        sol = self.data
        intersect = np.array(self.intersect).transpose()
        #Initiate
        fig = plt.figure(figsize=plt.figaspect(0.5))
        ax = fig.add_subplot(1, 2, 1, projection='3d')
        # First plot of figure and points
        ax.plot(sol[dim[0]],sol[dim[1]],sol[dim[2]],'b',linewidth=0.5,alpha = 0.9 )
        ax.plot(intersect[dim[0]],intersect[dim[1]],intersect[dim[2]],'or',markersize=1,alpha = 0.4 )

        #Plot plane:
        # Plot planeself
        # Försökte göra plan, men skitsvårt
    #    plane = self.poincareMapper.getPlaneNorm()
    #    print(plane)
    #    if plane[0] !=0:
    #        zz, yy = np.meshgrid(range(ax.get_zlim()),range(ax.get_ylim))
    #        xx = (-plane[1]*yy - plane[2]*zz)/plane[0]
    #        ax.plot_surface(xx, yy, zz, alpha=0.2)
        #Second plot of poincare planeself.
        ax = fig.add_subplot(1, 2, 2)
        z = self.poincareMapper.iterationdifference(func = fun)
        ax.plot(z[1],z[0],'or',markersize =3)
        x = np.linspace(*ax.get_xlim())
        ax.plot(x, x,'-b',alpha=0.2)


        plt.show()
