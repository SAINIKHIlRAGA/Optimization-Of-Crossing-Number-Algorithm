from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy


def decimaltobinary(a):
    k = 0
    b = list()
    while a >= 1:
        b.append(a % 2)
        a //= 2
        k += 1
    for i in range(k, 8):
        b.append(0)
    return b


img = Image.open('103_5.tif', 'r')
pix_vals = list(img.getdata())
L = 256
new_pix1 = list()
new_pix2 = list()
new_pix3 = list()
new_pix4 = list()
new_pix5 = list()
new_pix6 = list()
new_pix7 = list()
new_pix8 = list()

for i in pix_vals:
    c = decimaltobinary(i)
    new_pix1.append(c[0])
    new_pix2.append(c[1])
    new_pix3.append(c[2])
    new_pix4.append(c[3])
    new_pix5.append(c[4])
    new_pix6.append(c[5])
    new_pix7.append(c[6])
    new_pix8.append(c[7])

plt.imsave('bitplaneslice1.png', numpy.array(new_pix1).reshape(374, 388), cmap=cm.gray)
img1 = Image.open('bitplaneslice1.png', 'r')
plt.imsave('bitplaneslice2.png', numpy.array(new_pix2).reshape(374, 388), cmap=cm.gray)
img2 = Image.open('bitplaneslice2.png', 'r')
plt.imsave('bitplaneslice3.png', numpy.array(new_pix3).reshape(374, 388), cmap=cm.gray)
img3 = Image.open('bitplaneslice3.png', 'r')
plt.imsave('bitplaneslice4.png', numpy.array(new_pix4).reshape(374, 388), cmap=cm.gray)
img4 = Image.open('bitplaneslice4.png', 'r')
plt.imsave('bitplaneslice5.png', numpy.array(new_pix5).reshape(374, 388), cmap=cm.gray)
img5 = Image.open('bitplaneslice5.png', 'r')
plt.imsave('bitplaneslice6.png', numpy.array(new_pix6).reshape(374, 388), cmap=cm.gray)
img6 = Image.open('bitplaneslice6.png', 'r')
plt.imsave('bitplaneslice7.png', numpy.array(new_pix7).reshape(374, 388), cmap=cm.gray)
img7 = Image.open('bitplaneslice7.png', 'r')
plt.imsave('bitplaneslice8.png', numpy.array(new_pix8).reshape(374, 388), cmap=cm.gray)
img8 = Image.open('bitplaneslice8.png', 'r')

fig, ((ax0, ax1, ax2), (ax3, ax4, ax5), (ax6, ax7, ax8)) = plt.subplots(3, 3)
ax0.imshow(img, cmap='gray')
ax0.axis('off')
ax0.set_title('Original Image')
ax1.imshow(img1, cmap='gray')
ax1.axis('off')
ax1.set_title('Least Significant Bit')
ax2.imshow(img2, cmap='gray')
ax2.axis('off')
ax2.set_title('Bit Position = 2')
ax3.imshow(img3, cmap='gray')
ax3.axis('off')
ax3.set_title('Bit Position = 4')
ax4.imshow(img4, cmap='gray')
ax4.axis('off')
ax4.set_title('Bit Position = 8')
ax5.imshow(img5, cmap='gray')
ax5.axis('off')
ax5.set_title('Bit Position = 16')
ax6.imshow(img6, cmap='gray')
ax6.axis('off')
ax6.set_title('Bit Position = 32')
ax7.imshow(img7, cmap='gray')
ax7.axis('off')
ax7.set_title('Bit Position = 64')
ax8.imshow(img8, cmap='gray')
ax8.axis('off')
ax8.set_title('Most Significant Bit')
plt.show()
