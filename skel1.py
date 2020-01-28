import cv2
import numpy as np
from multiprocessing import Process
from PIL import Image
import matplotlib.cm as cm
import numpy
import matplotlib.pyplot as plt


def thresholding(pix_vals):
    for i in range(0, pix_vals.__len__()):
        pix_vals[i] = threshold(pix_vals[i])
    return pix_vals


def threshold(pix):
    if pix >= 128:
        return 1
    else:
        return 0


def skeletonization(input, output):
    img = cv2.imread(input, 0)
    size = np.size(img)
    skel = np.zeros(img.shape, np.uint8)

    ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    done = False

    while not done:
        eroded = cv2.erode(img, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()

        zeros = size - cv2.countNonZero(img)
        if zeros == size:
            done = True
    cv2.imwrite(output, skel)


if __name__ == '__main__':
    input = list()
    output = list()
    input.append("venv/101_1.tif")
    output.append("101_1_skel.tif")
    input.append("venv/101_2.tif")
    output.append("101_2_skel.tif")
    input.append("venv/101_3.tif")
    output.append("101_3_skel.tif")
    input.append("venv/101_4.tif")
    output.append("101_4_skel.tif")
    input.append("venv/101_5.tif")
    output.append("101_5_skel.tif")
    input.append("venv/101_6.tif")
    output.append("101_6_skel.tif")
    input.append("venv/101_7.tif")
    output.append("101_7_skel.tif")
    input.append("venv/101_8.tif")
    output.append("101_8_skel.tif")
    input.append("venv/102_1.tif")
    output.append("102_1_skel.tif")
    input.append("venv/102_2.tif")
    output.append("102_2_skel.tif")
    input.append("venv/102_3.tif")
    output.append("102_3_skel.tif")
    input.append("venv/102_4.tif")
    output.append("102_4_skel.tif")
    input.append("venv/102_5.tif")
    output.append("102_5_skel.tif")
    input.append("venv/102_6.tif")
    output.append("102_6_skel.tif")
    input.append("venv/102_7.tif")
    output.append("102_7_skel.tif")
    input.append("venv/102_8.tif")
    output.append("102_8_skel.tif")
    input.append("venv/103_1.tif")
    output.append("103_1_skel.tif")
    input.append("venv/103_2.tif")
    output.append("103_2_skel.tif")
    input.append("venv/103_3.tif")
    output.append("103_3_skel.tif")
    input.append("venv/103_4.tif")
    output.append("103_4_skel.tif")

    img = Image.open(input[0], 'r')
    pix_vals = list(img.getdata())
    pix_vals = thresholding(pix_vals)
    plt.imsave('try.png', numpy.array(pix_vals).reshape(374, 388), cmap=cm.gray)

    processes = []
    for i in range(1):
        processes.append(Process(target=skeletonization, args=('try.png', 'try1.tif',)))

    for process in processes:
        process.start()
    for process in processes:
        process.join()
        
    print("Completed")
