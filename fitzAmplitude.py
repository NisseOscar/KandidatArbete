import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import seaborn as sns
##################Generate data
###  Random sample
# start = np.random.rand(100)
# fitzData = [start]
# for i in range(0,1000): rtol = rtol, atol = atol
#     fitzData.append(fitzData[i]+0.3*np.random.rand(100))
####  Load data
fitzData = np.loadtxt('Fitz2Data.txt')
time = np.loadtxt('Time.txt')

fitzData = [np.linalg.norm(point) for point in fitzData]
print(fitzData)

plt.plot(fitzData,linewidth=0.7,alpha = 0.8)
plt.xlabel('time')
plt.ylabel('Norm of values')
plt.show()
