import os
from multiprocessing import Process, current_process
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy
import cv2
import math
import datetime


img = Image.open('101_1.tif', 'r')
pix_vals = list(img.getdata())
L = 256
new_pix = []
new_pix1 = []
new_pix2 = []
new_pix3 = []
new_pix4 = []


def negative1(pix_vals, new_pix):
    a = datetime.datetime.now()
    print(a)
    for i in range(0, 36278):
        new_pix1.append(L - 1 - pix_vals[i])
    # print(new_pix1.__len__())
    b = datetime.datetime.now()
    print(b)
    print(b - a)


def negative2(pix_vals, new_pix):
    for i in range(36278, 72556):
        new_pix2.append(L - 1 - pix_vals[i])
    # print(new_pix2.__len__())


def negative3(pix_vals, new_pix):
    for i in range(72556, 108834):
        new_pix3.append(L - 1 - pix_vals[i])
    # print(new_pix3.__len__())


def negative4(pix_vals, new_pix):
    for i in range(108834, 145112):
        new_pix4.append(L - 1 - pix_vals[i])
    # print(new_pix4.__len__())


if __name__ == '__main__':
    processes = []
    # a = datetime.datetime.now()
    # print(a)
    process1 = Process(target=negative1, args=(pix_vals, new_pix1))
    processes.append(process1)
    process1.start()

    process2 = Process(target=negative2, args=(pix_vals, new_pix2))
    processes.append(process2)
    process2.start()

    process3 = Process(target=negative3, args=(pix_vals, new_pix3))
    processes.append(process3)
    process3.start()

    process4 = Process(target=negative4, args=(pix_vals, new_pix4))
    processes.append(process4)
    process4.start()

    # b = datetime.datetime.now()
    # print(b)


# plt.imsave('negative_skeleton.png', numpy.array(new_pix).reshape(374, 388), cmap=cm.gray)
# img_out = cv2.imread('negative_skeleton.png', 0)
#
# cv2.imwrite('skeleton_negative.tif', img_out)
# img1 = Image.open('negative.png', 'r')
# fig, (ax0, ax1) = plt.subplots(1, 2)
# ax0.imshow(img, cmap='gray')
# ax0.axis('off')
# ax0.set_title('Original Image')
# ax1.imshow(img1, cmap='gray')
# ax1.axis('off')
# ax1.set_title('Negative')
# plt.show()
#
