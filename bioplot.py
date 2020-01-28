import matplotlib.pyplot as plt

x = ['FAR', 'FRR', 'TOTAL']
y = [20, 30, 40]
y_pos = [10, 12.5, 15]
plt.ylim(0, 60)
plt.bar(y_pos, y, color=['green', 'blue', 'orange'])
plt.xlabel('ERROR RATE')
plt.ylabel('PERCENTAGE', fontsize=5)

plt.xticks(y_pos, x)
plt.yticks()
plt.title('ERROR RATE WITHOUT ORIENTATION')
plt.show()

