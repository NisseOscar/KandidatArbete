import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import seaborn as sns
#Generate data
start = np.random.rand(100)
fitzData = [start]
for i in range(0,1000):
    fitzData.append(fitzData[i]+0.3*np.random.rand(100))


########### Plotting ######################
fig,ax = plt.subplots()
minimums = [min(point) for point in fitzData]
maximums = [max(point) for point in fitzData]
min = min(minimums)
max = max(maximums)
print(max)
print(min)
def animate(i):
    # ax.clear()
    # ax.contourf(xx,yy,np.split(fitzData[i],10))
    ax.clear()
    sns.heatmap(np.split(fitzData[i],10),cbar = False,ax=ax,cmap = 'Blues')


ani = animation.FuncAnimation(
    fig, animate,len(fitzData), interval=0.1, blit=False, save_count=50)

plt.show()
