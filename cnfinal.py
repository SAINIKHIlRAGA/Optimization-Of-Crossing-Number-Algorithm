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


def crossing_num_calc(a):
    collection = []
    feature_vector = {}
    isolate_point = 0
    ridge_ending = 0
    continuing_ridge = 0
    bifurcation_point = 0
    crossing_point = 0
    q = 0
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
            q += 1
    print(q)
    return collection, isolate_point, ridge_ending, continuing_ridge, bifurcation_point, crossing_point


def crossing_number_algorithm(img, file1, file2):
    img = Image.open(img, 'r')
    pix_vals = list(img.getdata())
    pix_vals = thresholding(pix_vals)
    new_pix = pix_vals
    new_pix1 = padding(new_pix)
    a = two_dim(new_pix1)
    collection, isolate_point, ridge_ending, continuing_ridge, bifurcation_point, crossing_point = crossing_num_calc(a)
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


if __name__ == '__main__':img1 = "101_1_skel.tif"
    file11 = "101_1_Feature_Vector.txt"
    file12 = "101_1_Point_Summary.txt"
    files11 = "101_1_Feature_Vector_series.txt"
    files12 = "101_1_Point_Summary_series.txt"
    img2 = "101_2_skel.tif"
    file21 = "101_2_Feature_Vector.txt"
    file22 = "101_2_Point_Summary.txt"
    files21 = "101_2_Feature_Vector_series.txt"
    files22 = "101_2_Point_Summary_series.txt"
    img3 = "101_3_skel.tif"
    file31 = "101_3_Feature_Vector.txt"
    file32 = "101_3_Point_Summary.txt"
    files31 = "101_3_Feature_Vector_series.txt"
    files32 = "101_3_Point_Summary_series.txt"
    img4 = "101_4_skel.tif"
    file41 = "101_4_Feature_Vector.txt"
    file42 = "101_4_Point_Summary.txt"
    files41 = "101_4_Feature_Vector_series.txt"
    files42 = "101_4_Point_Summary_series.txt"
    img5 = "101_5_skel.tif"
    file51 = "101_5_Feature_Vector.txt"
    file52 = "101_5_Point_Summary.txt"
    files51 = "101_5_Feature_Vector_series.txt"
    files52 = "101_5_Point_Summary_series.txt"
    start1 = time.time()
    processes = []
    process1 = Process(target=crossing_number_algorithm, args=(img1, file11, file12,))
    process2 = Process(target=crossing_number_algorithm, args=(img2, file21, file22,))
    process3 = Process(target=crossing_number_algorithm, args=(img3, file31, file32,))
    process4 = Process(target=crossing_number_algorithm, args=(img4, file41, file42,))
    process5 = Process(target=crossing_number_algorithm, args=(img5, file51, file52,))
    processes.append(process1)
    processes.append(process2)
    processes.append(process3)
    processes.append(process4)
    processes.append(process5)
    process1.start()
    process2.start()
    process3.start()
    process4.start()
    process5.start()
    process1.join()
    process2.join()
    process3.join()
    process4.join()
    process5.join()
    stop1 = time.time()
    print("Parallel Execution Time is ", stop1-start1)

    start2 = time.time()
    crossing_number_algorithm(img1, files11, files12)
    crossing_number_algorithm(img2, files21, files22)
    crossing_number_algorithm(img3, files31, files32)
    crossing_number_algorithm(img4, files41, files42)
    crossing_number_algorithm(img5, files51, files52)
    stop2 = time.time()
    print("Sequential Execution Time is ", stop2-start2)
    print("Completed")







