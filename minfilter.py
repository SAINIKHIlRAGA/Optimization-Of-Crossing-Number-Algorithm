from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy
import math
import time


def find_min(a):
    minimum = a[0]
    for i in a:
        if i < minimum:
            minimum = i
    return minimum


img = Image.open('103_5.tif', 'r')
pix_vals = list(img.getdata())

new_pix = list()
new_pix1 = list()
for i in pix_vals:
    new_pix.append(i)

new_pix1.append(new_pix[0])
for i in range(0, 388):
    new_pix1.append(new_pix[i])
new_pix1.append(new_pix[387])

k = 0
for j in range(0, 374):
    new_pix1.append(new_pix[j*388])
    for i in range(0, 388):
        new_pix1.append(new_pix[k])
        k += 1
    new_pix1.append(new_pix[(j+1)*387])

new_pix1.append(new_pix[373*388])
for i in range(0, 388):
    new_pix1.append(new_pix[i])
new_pix1.append(new_pix[374*387])
avg = 0
new_pix2 = list()

a = list()
q = 0
for i in range(0, 376):
    b = list()
    for j in range(0, 390):
        b.append(new_pix1[q])
        q += 1
    a.append(b)
t1 = time.time()

c = list()
for i in range(1, 375):
    for j in range(1, 389):
        min = find_min([a[i-1][j-1], a[i-1][j], a[i-1][j+1], a[i][j-1], a[i][j], a[i][j+1], a[i+1][j-1], a[i+1][j], a[i+1][j+1]])//9
        c.append(min)

t2 = time.time()
print("Total Time taken : ", t2-t1)

plt.imsave('average.png', numpy.array(c).reshape(374, 388), cmap=cm.gray)
img1 = Image.open('average.png', 'r')
fig, (ax0, ax1) = plt.subplots(1, 2)
ax0.imshow(img, cmap='gray')
ax0.axis('off')
ax0.set_title('Original Image')
ax1.imshow(img1, cmap='gray')
ax1.axis('off')
ax1.set_title('Average')
plt.show()
