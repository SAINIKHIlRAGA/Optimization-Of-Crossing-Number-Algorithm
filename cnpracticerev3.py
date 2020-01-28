from PIL import Image
import os
import time
from multiprocessing import Process, Pool, current_process


def thresholding(pix_vals):
    for i in range(0, pix_vals.__len__()):
        pix_vals[i] = threshold(pix_vals[i])
    return pix_vals


def threshold(pix):
    if pix >= 128:
        return 1
    else:
        return 0


def padding(new_pix):
    pix = list()
    pix.append(new_pix[0])
    for i in range(0, 388):
        pix.append(new_pix[i])
    pix.append(new_pix[387])
    k = 0
    for j in range(0, 374):
        pix.append(new_pix[j * 388])
        for i in range(0, 388):
            pix.append(new_pix[k])
            k += 1
        pix.append(new_pix[(j + 1) * 387])
    pix.append(new_pix[373 * 388])
    for i in range(0, 388):
        pix.append(new_pix[i])
    pix.append(new_pix[374 * 387])
    return pix


def two_dim(pix):
    a = list()
    q = 0
    for i in range(0, 376):
        b = list()
        for j in range(0, 390):
            b.append(pix[q])
            q += 1
        a.append(b)
    return a


def calc_i(i, a):
    collection = []
    feature_vector = {}
    continuing_ridge = 0
    bifurcation_point = 0
    isolate_point = 0
    ridge_ending = 0
    crossing_point = 0
    for j in range(1, 389):
        sum = 0
        if a[i][j] == 1:
            sum += (abs(a[i - 1][j - 1] - a[i][j - 1]) + abs(a[i][j - 1] - a[i + 1][j - 1]) + abs(
                a[i + 1][j - 1] - a[i + 1][j]) + abs(a[i + 1][j] - a[i + 1][j + 1]) + abs(
                a[i + 1][j + 1] - a[i][j + 1]) + abs(a[i][j + 1] - a[i - 1][j + 1]) + abs(
                a[i - 1][j + 1] - a[i - 1][j]) + abs(a[i - 1][j] - a[i - 1][j - 1])) / 2
            if sum == 0:
                isolate_point += 1
                feature_vector = {"position_x": i, "position_y": j, "type": "isolate_point"}
            elif sum == 1:
                ridge_ending += 1
                feature_vector = {"position_x": i, "position_y": j, "type": "ridge_ending"}
            elif sum == 2:
                continuing_ridge += 1
                feature_vector = {"position_x": i, "position_y": j, "type": "continuing_ridge"}
            elif sum == 3:
                bifurcation_point += 1
                feature_vector = {"position_x": i, "position_y": j, "type": "bifurcation_point"}
            elif sum == 4:
                crossing_point += 1
                feature_vector = {"position_x": i, "position_y": j, "type": "crossing_point"}
            collection.append(feature_vector)


def crossing_num_calc2(a):
    collection = []
    feature_vector = {}
    isolate_point = 0
    ridge_ending = 0
    continuing_ridge = 0
    bifurcation_point = 0
    crossing_point = 0
    for i in range(1, 375):
        for j in range(1, 389):
            sum = 0
            if a[i][j] == 1:
                sum += (abs(a[i - 1][j - 1] - a[i][j - 1]) + abs(a[i][j - 1] - a[i + 1][j - 1]) + abs(
                    a[i + 1][j - 1] - a[i + 1][j]) + abs(a[i + 1][j] - a[i + 1][j + 1]) + abs(
                    a[i + 1][j + 1] - a[i][j + 1]) + abs(a[i][j + 1] - a[i - 1][j + 1]) + abs(
                    a[i - 1][j + 1] - a[i - 1][j]) + abs(a[i - 1][j] - a[i - 1][j - 1])) / 2
                if sum == 0:
                    isolate_point += 1
                    feature_vector = {"position_x": i, "position_y": j, "type": "isolate_point"}
                elif sum == 1:
                    ridge_ending += 1
                    feature_vector = {"position_x": i, "position_y": j, "type": "ridge_ending"}
                elif sum == 2:
                    continuing_ridge += 1
                    feature_vector = {"position_x": i, "position_y": j, "type": "continuing_ridge"}
                elif sum == 3:
                    bifurcation_point += 1
                    feature_vector = {"position_x": i, "position_y": j, "type": "bifurcation_point"}
                elif sum == 4:
                    crossing_point += 1
                    feature_vector = {"position_x": i, "position_y": j, "type": "crossing_point"}
                collection.append(feature_vector)
    return collection, isolate_point, ridge_ending, continuing_ridge, bifurcation_point, crossing_point


def crossing_num_calc1(a):
    collection = []
    feature_vector = {}
    continuing_ridge = 0
    bifurcation_point = 0
    isolate_point = 0
    ridge_ending = 0
    crossing_point = 0
    l = range(1, 375)
    p = Pool(3)
    a = a

    res = [p.apply(calc_i, args=(i, a)) for i in l]
    # for i in range(1, 375):

    return collection, isolate_point, ridge_ending, continuing_ridge, bifurcation_point, crossing_point


def crossing_number_algorithm1(img, file1, file2):
    img = Image.open(img, 'r')
    pix_vals = list(img.getdata())
    pix_vals = thresholding(pix_vals)
    new_pix = pix_vals
    new_pix1 = padding(new_pix)
    a = two_dim(new_pix1)
    collection, isolate_point, ridge_ending, continuing_ridge, bifurcation_point, crossing_point = crossing_num_calc1(a)
    sum_all = isolate_point + ridge_ending + continuing_ridge + bifurcation_point + crossing_point
    pixel_type_collection = {"Isolated Points": isolate_point, "Ridge Ending Points": ridge_ending,
                             "Ridge Continuing Points": continuing_ridge, "Bifurcation Points": bifurcation_point,
                             "Crossing Points": crossing_point, "Total Points": sum_all}

    with open(file1, "w") as f:
        for fv in collection:
            f.write(str(fv))
            f.write("\n")
    f.close()
    with open(file2, "w") as f:
        f.write(str(pixel_type_collection))


def crossing_number_algorithm2(img, file1, file2):
    img = Image.open(img, 'r')
    pix_vals = list(img.getdata())
    pix_vals = thresholding(pix_vals)
    new_pix = pix_vals
    new_pix1 = padding(new_pix)
    a = two_dim(new_pix1)
    collection, isolate_point, ridge_ending, continuing_ridge, bifurcation_point, crossing_point = crossing_num_calc2(a)
    sum_all = isolate_point + ridge_ending + continuing_ridge + bifurcation_point + crossing_point
    pixel_type_collection = {"Isolated Points": isolate_point, "Ridge Ending Points": ridge_ending,
                             "Ridge Continuing Points": continuing_ridge, "Bifurcation Points": bifurcation_point,
                             "Crossing Points": crossing_point, "Total Points": sum_all}

    with open(file1, "w") as f:
        for fv in collection:
            f.write(str(fv))
            f.write("\n")
    f.close()
    with open(file2, "w") as f:
        f.write(str(pixel_type_collection))


if __name__ == '__main__':
    img1 = Image.open('101_1_skel.tif', 'r')
    img1 = "101_1_skel.tif"
    file11 = "101_1_Feature_Vector_InnerParallel.txt"
    file12 = "101_1_Point_Summary_InnerParallel.txt"
    file21 = "101_1_Feature_Vector_InnerSerial.txt"
    file22 = "101_1_Point_Summary_InnerSerial.txt"
    start1 = time.time()
    crossing_number_algorithm1(img1, file11, file12)
    stop1 = time.time()
    print("Parallel Execution Time is ", stop1 - start1)
    start2 = time.time()
    crossing_number_algorithm2(img1, file21, file22)
    stop2 = time.time()
    print("Sequential Execution Time is ", stop2-start2)







