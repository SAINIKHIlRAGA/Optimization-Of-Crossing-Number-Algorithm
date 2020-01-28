import matplotlib.pyplot as plt

# line 1 points
from scipy.constants import alpha

x1 = [1, 2, 5, 10, 15, 20]
y1 = [1.1405494213104248, 1.5438673496246338, 3.0997023582458496, 5.9500720500946045, 8.498252868652344, 13.529784202575684]
y2 = [1.0990567207336426, 2.082425117492676, 5.599013328552246, 11.86723518371582, 19.319289922714233, 24.744818210601807]

# plotting the line 1 points
plt.plot(x1, y1, label="Parallel Execution")
plt.plot(x1, y1, 'bo')

# plotting the line 2 points
plt.plot(x1, y2, label="Sequential Execution")
plt.plot(x1, y2, 'ro')
plt.axis([1, 25, 0.001, 30])
# naming the x axis
plt.xlabel('Number of FingerPrints')
# naming the y axis
plt.ylabel('Time Taken(in sec)')
# giving a title to my graph
plt.title('Time vs Number of Fingerprints Being Matched Graph')

# show a legend on the plot
plt.legend()

# function to show the plot
plt.show()
