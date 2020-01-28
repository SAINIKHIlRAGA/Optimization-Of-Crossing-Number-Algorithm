import matplotlib.pyplot as plt

# line 1 points
from scipy.constants import alpha

x1 = [1, 2, 5, 10, 15, 20, 30, 40, 50]
y1 = [0.4996628761291504, float(0.7469878196716309), 1.0076236724853516, 2.4654011726379395, 3.328091621398926, 4.781199932098389, 6.958374500274658, 9.021849393844604, 11.386521100997925]
y2 = [0.35704493522644043, 0.5852251052856445, 1.6679506301879883, 4.186087369918823, 6.369455337524414, 8.5143723487854, 14.083029747009277, 22.34259557723999, 25.790124893188477]

# plotting the line 1 points
plt.plot(x1, y1, label="Parallel Execution")
plt.plot(x1, y1, 'bo')

# plotting the line 2 points
plt.plot(x1, y2, label="Sequential Execution")
plt.plot(x1, y2, 'ro')
plt.axis([1, 70, 0.001, 50])
# naming the x axis
plt.xlabel('Number of FingerPrints')
# naming the y axis
plt.ylabel('Time Taken(in sec)')
# giving a title to my graph
plt.title('Time vs Number of Fingerprints Graph')

# show a legend on the plot
plt.legend()

# function to show the plot
plt.show()
