import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes

class GraphSeparetor:
    def __init__(self, data, n_neighbors):
        self.data = data

    # Set all points that belong to the lower crurve to one
    def ConstructGraph(self, sepRight, sepLeft, incRight, incLeft, tol_merged):
        lowerCurve = np.zeros(len(self.data[:,1]))
        # Right branch
        for i in range(0,len(sepRight)-1):
            # TODO tol!!
            # Add all points on the right branch in the merged section to the lower curve
            indexPoints = np.where((self.data[:,1] <= sepRight[i,1]) & (self.data[:,1] >= sepRight[i+1,1]) & (self.data[:,0] > sepRight[i,0]-0.005) & (self.data[:,0] > sepRight[0,0]))
            print(sepRight[i+1,1])
            if self.isMergedRight(incRight, sepRight, i, tol_merged):
                lowerCurve[indexPoints] = 1
            # Add all points below the right separator to the lower curve
            else:
                for point in indexPoints[0]:
                    if self.data[point,1] <  sepRight[i,1] + incRight[i] * (self.data[point,0] - sepRight[i,0]):
                        lowerCurve[point] = 1
        # Left branch
        for i in range(0,len(sepLeft)-1):
            # Add all points on the left branchin the merged section to the lower curve
            indexPoints = np.where((self.data[:,1] <= sepLeft[i,1]) & (self.data[:,1] >= sepLeft[i+1,1]) & (self.data[:,0] < sepLeft[i,0]+0.005) & (self.data[:,0] < sepLeft[0,0]))
            if self.isMergedLeft(incLeft, sepLeft, i, tol_merged):
                lowerCurve[indexPoints] = 1
            # Add all points below the left separator to the lower curve
            else:
                for point in indexPoints[0]:
                    if self.data[point,1] <  sepLeft[i,1] + incLeft[i] * (self.data[point,0] - sepLeft[i,0]):
                        lowerCurve[point] = 1
        below = np.where((self.data[:,1] < sepLeft[i,1]) & (self.data[:,1] < sepLeft[i,1]))
        lowerCurve[below] = 1
        return lowerCurve


    # Calculate distance from point to the closest point on the separator
    def distFromSep(self, inclination, separator, point, i):
        x = (point[1] + point[0]/inclination[i] - separator[i,1] + inclination[i]*separator[i,0])/(inclination[i] + 1/inclination[i])
        y =  separator[i,1] + inclination[i] * (x - separator[i,0])
        return np.sqrt((x - point[0])**2  + (y - point[1])**2)

    # Returns the inidices og all points above the separator
    def pointsAboveSeparator(self, inclination, separator,i):
        return self.data[:,1] >=  inclination[i] * (self.data[:,0] - separator[i,0]) + separator[i,1]

    # Returns the inidices og all points below the separator
    def pointsBelowSeparator(self, inclination, separator, i):
        return self.data[:,1] <=  inclination[i] * (self.data[:,0] - separator[i,0]) + separator[i,1]

    # Returns true if the points mean of the points on both side of the right separator segment is closer to the separator than tol_merged
    def isMergedRight(self, inclination, separator, i, tol_merged):
        top = np.where((self.data[:,0] > separator[i-1,0]) & (self.data[:,1] < separator[i-1,1]) & (self.data[:,1] > separator[i,1]) & self.pointsAboveSeparator(inclination, separator, i))
        bottom = np.where((self.data[:,0] > separator[i-1,0]) & (self.data[:,1] < separator[i-1,1]) & (self.data[:,1] > separator[i,1]) &  self.pointsBelowSeparator(inclination, separator, i))

        if np.size(top) < 1 or np.size(bottom) < 1:
            if np.size(top) > 1:
                bottom = top
            elif np.size(bottom) > 1:
                top = bottom
            else:
                return False

        topMean = [np.mean(self.data[top,0]), np.mean(self.data[top,1])]
        bottomMean = [np.mean(self.data[bottom,0]), np.mean(self.data[bottom,1])]

        return self.distFromSep(inclination, separator, topMean, i-1) < tol_merged and self.distFromSep(inclination, separator, bottomMean, i-1) < tol_merged

    # Returns true if the points mean of the points on both side of the right separator segment is closer to the separator than tol_merged
    def isMergedLeft(self, inclination, separator, i, tol_merged):

        top = np.where((self.data[:,0] < separator[i-1,0]) & (self.data[:,1] < separator[i-1,1]) & (self.data[:,1] > separator[i,1]) & self.pointsAboveSeparator(inclination, separator, i))
        bottom = np.where((self.data[:,0] < separator[i-1,0]) & (self.data[:,1] < separator[i-1,1]) & (self.data[:,1] > separator[i,1]) &  self.pointsBelowSeparator(inclination, separator, i))

        if np.size(top) < 1 or np.size(bottom) < 1:
            if np.size(top) > 1:
                bottom = top
            elif np.size(bottom) > 1:
                top = bottom
            else:
                return False

        topMean = [np.mean(self.data[top,0]), np.mean(self.data[top,1])]
        bottomMean = [np.mean(self.data[bottom,0]), np.mean(self.data[bottom,1])]

        return self.distFromSep(inclination, separator, topMean, i-1) < tol_merged and self.distFromSep(inclination, separator, bottomMean, i-1) < tol_merged
    # Finds one of the points on the top of the lower curve
    def findSecondCurve(self, sections, tol_middlePoint):
        for i in range(1,len(sections)):
            sections = sections[::-1]
            # Find the points furthest to the right an left for each section
            indexMax = int(np.argmax(np.where((self.data[:,1] > sections[i]) & (self.data[:,1] < sections[i-1]), self.data[:,0], -np.Inf)))
            indexMin = int(np.argmin(np.where((self.data[:,1] > sections[i]) & (self.data[:,1] < sections[i-1]), self.data[:,0], np.Inf)))
            right = self.data[indexMax,0]
            left = self.data[indexMin,0]
            dist = (right - left) /2
            # Checks if there is any points between the upper curve and choses the maximum of them
            middlePoints  = np.argmax(np.where((self.data[:,0]<left + dist + tol_middlePoint * dist) & (self.data[:,0] > left + dist - tol_middlePoint * dist) & (self.data[:,1] > sections[i]) & (self.data[:,1] < sections[i-1]), 1, 0))
            # Returns the middle points with largest y-value, if there exist any
            if middlePoints > 0:
                #plt.scatter(self.data[middlePoints,0], self.data[middlePoints,1], c ='r')
                return middlePoints, i
    # Constructs one right and one left separator to separate the lower and upp curve from each other
    def constructSeparators(self, tol_merged, tol_middlePoint, tol_int, nbr_int):
        # tol_merged: Tolerance for how close the graphs need to be to be inseparable
        # tol_middlePoint: Tolerance for how large intervals we look for the max value of the lower graph
        # tol_int: Tolerance for how large intervals we look for points when constructing the middle sepectory
        # tol_int: Number of sections that the graphs are devided into

        indexMaxTopGraph = np.argmax(self.data[:,1])

        # Construct a uniformly distributed interval from the highest to the lowest point
        sections = np.linspace(np.min(self.data[:,1]), np.max(self.data[:,1]), nbr_int)[::-1]

        [startIndexLowerGraph, startSection] = self.findSecondCurve(sections, tol_middlePoint)
        #startIndexLowerGraph = np.where((self.data[:,0] > 0.0425) & (self.data[:,0] < 0.0430) & (self.data[:,1] > 0.0612) & (self.data[:,1] < 0.062))
        #dat =  self.data[startIndexLowerGraph,1]
        # print(dat)
        # print(np.where(sections < dat)[1])
        #startSection = np.min(np.where(sections < dat)[1])
        #print(startSection)
        # print(sections)

        countRight = 1
        countLeft = 1

        # Separators for the right and left branch
        sepRight = np.zeros((nbr_int-startSection+1,2))
        sepLeft = np.zeros((nbr_int-startSection+1,2))

        # The inclination in each section
        incRight = np.zeros(nbr_int-startSection)
        incLeft = np.zeros(nbr_int-startSection)

        # Set a value between the max values of the two graphs as start values
        startPointX = self.data[startIndexLowerGraph,0] +  (self.data[indexMaxTopGraph,0] - self.data[startIndexLowerGraph,0]) / 20
        startPointY = self.data[startIndexLowerGraph,1] +  (self.data[indexMaxTopGraph,1] - self.data[startIndexLowerGraph,1]) / 20
        xPrevRight = startPointX
        xPrevLeft = startPointX
        sepRight[0,:] = [startPointX, startPointY]
        sepLeft[0,:] = [startPointX, startPointY]
        print(startPointX)

        for i in range(startSection, nbr_int-1):
            # Finda all points
            right = np.where((self.data[:,0]>xPrevRight) & (self.data[:,1] > sections[i] - tol_int) & (self.data[:,1] < sections[i] + tol_int))
            left = np.where((self.data[:,0]<xPrevLeft) & (self.data[:,1] > sections[i] - tol_int) & (self.data[:,1] < sections[i] + tol_int))
            #print(sections[i] - tol_int)
            #print(sections[i] + tol_int)

            if np.size(right) > 0:
                #print(right)
                right = right[0]
                #print(right)
                indexTopRight = np.argmax(self.data[right,0])
                indexBottomRight = np.argmin(self.data[right,0])
                if indexTopRight != indexBottomRight:
                    sepRight[countRight,0] = (self.data[right[indexTopRight],0] +self.data[right[indexBottomRight],0])/2
                    sepRight[countRight,1] = (self.data[right[indexTopRight],1] + self.data[right[indexBottomRight],1])/2

                    incRight[countRight-1] = (sepRight[countRight,1] - sepRight[countRight -1,1]) / (sepRight[countRight ,0] - sepRight[countRight -1,0])
                    xPrevRight = self.data[right[indexBottomRight],0]
                    countRight = countRight + 1

            if  np.size(left) > 0:

                left = left[0]
                indexTopLeft = np.argmax(self.data[left,0])
                indexBottomLeft = np.argmin(self.data[left,0])
                if indexTopRight != indexBottomRight:
                    sepLeft[countLeft,0] = (self.data[left[indexTopLeft],0] + self.data[left[indexBottomLeft],0])/2
                    sepLeft[countLeft,1] = (self.data[left[indexTopLeft],1] + self.data[left[indexBottomLeft],1])/2

                    incLeft[countLeft-1] = (sepLeft[countLeft,1] - sepLeft[countLeft-1,1]) / (sepLeft[countLeft,0] - sepLeft[countLeft-1,0])
                    xPrevLeft = self.data[left[indexTopLeft],0]
                    countLeft = countLeft + 1

        sepRight[countRight] = self.data[np.argmax(self.data[:,0])]
        sepLeft[countLeft] = self.data[np.argmin(self.data[:,0])]
        incRight[countRight-1] = (sepRight[countRight,1] - sepRight[countRight -1,1]) / (sepRight[countRight ,0] - sepRight[countRight -1,0])
        incLeft[countLeft-1] = (sepLeft[countLeft,1] - sepLeft[countLeft-1,1]) / (sepLeft[countLeft,0] - sepLeft[countLeft-1,0])

        return sepRight[:countRight+1], sepLeft[:countLeft+1], incRight[:countRight+1], incLeft[:countLeft+1]

    def SeperateGraphs(self, colPlot, tol_merged, tol_middlePoint, tol_int, nbr_int):
        [sepRight, sepLeft, incRight, incLeft] = self.constructSeparators(tol_merged, tol_middlePoint, tol_int, nbr_int)

        # # 1 if data point j belongs to graph i, zero otherwise. i in nbr graphs, j in nbr datapoints
        graphMatrix = np.zeros((2,len(self.data)))

        # Construct lower graph
        lowerGraph = self.ConstructGraph(sepRight, sepLeft, incRight, incLeft, tol_merged)
        symbols = np.where(lowerGraph>0,"u","l")

        if colPlot:
            # fig = plt.figure()
            # ax = fig.add_subplot(121)
            # ax.scatter(self.data[:,0],self.data[:,1], s=2)
            # ax.plot(sepRight[:,0], sepRight[:,1], 'black')
            # ax.plot(sepLeft[:,0], sepLeft[:,1], 'black')
            #
            # ax = fig.add_subplot(122)
            # col = np.where(symbols == 'u','navy','cornflowerblue')
            # ax.scatter(self.data[:,0],self.data[:,1],c=col, s=2)
            # #plt.plot(sepRight[:,0], sepRight[:,1], 'black')
            # #plt.plot(sepLeft[:,0], sepLeft[:,1], 'black')
            #
            #
            # axins = zoomed_inset_axes(ax, 6, loc=1) # zoom-factor: 2.5, location: upper-left
            # axins.scatter(self.data[:,0],self.data[:,1],c=col, s=2)
            # x1, x2, y1, y2 = 0.052, 0.058, 0.037, 0.047 # specify the limits
            # x = [x1, x1, x2, x2, x1]
            # y = [y1, y2, y2, y1, y1]
            # ax.plot(x,y, 'black')
            # axins.set_xlim(x1, x2) # apply the x-limits
            # axins.set_ylim(y1, y2) # apply the y-limits
            # plt.yticks(visible=False)
            # plt.xticks(visible=False)
            # plt.show()
            #


            fig = plt.figure()
            ax = fig.add_subplot(121)
            lowerCurve = np.where(symbols == 'l')
            ax.scatter(self.data[lowerCurve,0], self.data[lowerCurve,1], c ='navy', s=2)
            ax.set_xlim([0,0.125])
            ax.set_ylim([0,0.12])

            ax = fig.add_subplot(122)
            upperCurve = np.where(symbols == 'u')
            ax.scatter(self.data[upperCurve,0], self.data[upperCurve,1], c='cornflowerblue', s=2)
            ax.set_xlim([0,0.125])
            ax.set_ylim([0,0.12])
            plt.show()


        return symbols
