from PIL import Image
import time
from multiprocessing import Process
import threading
import math

a = list()
collection = []
continuing_ridge = 0
bifurcation_point = 0
isolate_point = 0
ridge_ending = 0
crossing_point = 0
valid_bifurcation_point = 0
valid_ridge_ending = 0


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


def calc_i(start, end):
    global collection
    global continuing_ridge
    global bifurcation_point
    global isolate_point
    global ridge_ending
    global crossing_point
    global valid_bifurcation_point
    global valid_ridge_ending

    feature_vector = {}
    lock = threading.Lock()
    for i in range(start, end):
        for j in range(1, 389):
            sum = 0
            o = 0
            if a[i][j] == 1:
                sum += (abs(a[i - 1][j - 1] - a[i][j - 1]) + abs(a[i][j - 1] - a[i + 1][j - 1]) + abs(
                    a[i + 1][j - 1] - a[i + 1][j]) + abs(a[i + 1][j] - a[i + 1][j + 1]) + abs(
                    a[i + 1][j + 1] - a[i][j + 1]) + abs(a[i][j + 1] - a[i - 1][j + 1]) + abs(
                    a[i - 1][j + 1] - a[i - 1][j]) + abs(a[i - 1][j] - a[i - 1][j - 1])) / 2
                if sum == 0:
                    lock.acquire()
                    isolate_point += 1
                    lock.release()
                    feature_vector = {"position_x": i, "position_y": j, "type": "isolate_point"}
                elif sum == 1:
                    lock.acquire()
                    ridge_ending += 1
                    lock.release()
                    feature_vector = {"position_x": i, "position_y": j, "type": "ridge_ending"}
                elif sum == 2:
                    lock.acquire()
                    continuing_ridge += 1
                    lock.release()
                    feature_vector = {"position_x": i, "position_y": j, "type": "continuing_ridge"}
                elif sum == 3:
                    lock.acquire()
                    bifurcation_point += 1
                    lock.release()
                    feature_vector = {"position_x": i, "position_y": j, "type": "bifurcation_point"}
                elif sum == 4:
                    lock.acquire()
                    crossing_point += 1
                    lock.release()
                    feature_vector = {"position_x": i, "position_y": j, "type": "crossing_point"}
                lock.acquire()
                collection.append(feature_vector)
                lock.release()


def crossing_num_calc1(a):
    list1 = 375
    list2 = int(list1/4)
    list3 = int(list1/4*2)
    list4 = int(list1/4*3)
    threads = list()
    threads.append(threading.Thread(target=calc_i, args=(1, list2,)))
    threads.append(threading.Thread(target=calc_i, args=(list2+1, list3,)))
    threads.append(threading.Thread(target=calc_i, args=(list3+1, list4,)))
    threads.append(threading.Thread(target=calc_i, args=(list4+1, list1,)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return collection, continuing_ridge, bifurcation_point, isolate_point, ridge_ending, crossing_point


def crossing_num_calc2(a):
    global collection
    global isolate_point
    global ridge_ending
    global continuing_ridge
    global bifurcation_point
    global crossing_point
    global valid_bifurcation_point
    global valid_ridge_ending
    feature_vector = {}
    for i in range(1, 375):
        for j in range(1, 389):
            sum = 0
            o = 0
            if a[i][j] == 1:
                sum += (abs(a[i - 1][j - 1] - a[i][j - 1]) + abs(a[i][j - 1] - a[i + 1][j - 1]) + abs(
                    a[i + 1][j - 1] - a[i + 1][j]) + abs(a[i + 1][j] - a[i + 1][j + 1]) + abs(
                    a[i + 1][j + 1] - a[i][j + 1]) + abs(a[i][j + 1] - a[i - 1][j + 1]) + abs(
                    a[i - 1][j + 1] - a[i - 1][j]) + abs(a[i - 1][j] - a[i - 1][j - 1])) / 2
                if sum == 0:
                    isolate_point += 1
                    feature_vector = {"position_x": i, "position_y": j, "type": "isolate_point", "orientation": o}
                elif sum == 1:
                    ridge_ending += 1
                    b = i
                    c = j
                    while o < 360 and a[b + 1][c] != 1 and b < 373 and c < 388:
                        b += int(2 * (math.cos(o)))
                        c += int(2 * (math.sin(o)))
                        o += 1
                    if b == 374 or c == 388:
                        o = -1
                    feature_vector = {"position_x": i, "position_y": j, "type": "ridge_ending", "orientation": o}
                elif sum == 2:
                    continuing_ridge += 1
                    feature_vector = {"position_x": i, "position_y": j, "type": "continuing_ridge", "orientation": o}
                elif sum == 3:
                    bifurcation_point += 1
                    b = i
                    c = j
                    while o < 360 and a[b + 1][c] != 1 and b < 373 and c < 388:
                        b += int(2 * (math.cos(o)))
                        c += int(2 * (math.sin(o)))
                        o += 1
                    if b == 374 or c == 388:
                        o = -1
                    feature_vector = {"position_x": i, "position_y": j, "type": "bifurcation_point", "orientation": o}
                elif sum == 4:
                    crossing_point += 1
                    feature_vector = {"position_x": i, "position_y": j, "type": "crossing_point", "orientation": o}
                if (feature_vector['type'] == 'bifurcation_point' or feature_vector['type'] == 'ridge_ending') and (
                        feature_vector['orientation'] != 0 and feature_vector['orientation'] != 360 and feature_vector['orientation'] != -1):
                    if feature_vector['type'] == 'bifurcation_point':
                        valid_bifurcation_point += 1
                        feature_vector["type"] = "valid_bifurcation_point"
                    elif feature_vector['type'] == 'ridge_ending':
                        feature_vector["type"] = "valid_ridge_ending"
                        valid_ridge_ending += 1
                    collection.append(feature_vector)
    return collection, isolate_point, ridge_ending, continuing_ridge, bifurcation_point, crossing_point, valid_bifurcation_point, valid_ridge_ending


def crossing_number_algorithm1(img, file1, file2):
    global a
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
    global a
    img = Image.open(img, 'r')
    pix_vals = list(img.getdata())
    pix_vals = thresholding(pix_vals)
    new_pix = pix_vals
    new_pix1 = padding(new_pix)
    a = two_dim(new_pix1)
    collection, isolate_point, ridge_ending, continuing_ridge, bifurcation_point, crossing_point, valid_bifurcation_point, valid_ridge_ending = crossing_num_calc2(a)
    sum_all = isolate_point + ridge_ending + continuing_ridge + bifurcation_point + crossing_point
    pixel_type_collection = {"Isolated Points": isolate_point, "Ridge Ending Points": ridge_ending,
                             "Ridge Continuing Points": continuing_ridge, "Bifurcation Points": bifurcation_point,
                             "Crossing Points": crossing_point, "Total Points": sum_all,
                             "Valid Bifurcation Points": valid_bifurcation_point,
                             "Valid Ridge Ending Points": valid_ridge_ending}
    with open(file1, "w") as f:
        for fv in collection:
            f.write(str(fv))
            f.write("\n")
    f.close()
    with open(file2, "w") as f:
        f.write(str(pixel_type_collection))


if __name__ == '__main__':
    img = list()
    file_a = list()
    file_b = list()
    file_sa = list()
    file_sb = list()

    img.append("101_1_skel.tif")
    img.append("101_2_skel.tif")
    img.append("101_3_skel.tif")
    img.append("101_4_skel.tif")
    img.append("101_5_skel.tif")
    img.append("101_6_skel.tif")
    img.append("101_7_skel.tif")
    img.append("101_8_skel.tif")
    img.append("102_1_skel.tif")
    img.append("102_2_skel.tif")
    img.append("102_3_skel.tif")
    img.append("102_4_skel.tif")
    img.append("102_5_skel.tif")
    img.append("102_6_skel.tif")
    img.append("102_7_skel.tif")
    img.append("102_8_skel.tif")
    img.append("103_1_skel.tif")
    img.append("103_2_skel.tif")
    img.append("103_3_skel.tif")
    img.append("103_4_skel.tif")

    file_a.append("101_1_Feature_Vector.txt")
    file_a.append("101_2_Feature_Vector.txt")
    file_a.append("101_3_Feature_Vector.txt")
    file_a.append("101_4_Feature_Vector.txt")
    file_a.append("101_5_Feature_Vector.txt")
    file_a.append("101_6_Feature_Vector.txt")
    file_a.append("101_7_Feature_Vector.txt")
    file_a.append("101_8_Feature_Vector.txt")
    file_a.append("102_1_Feature_Vector.txt")
    file_a.append("102_2_Feature_Vector.txt")
    file_a.append("102_3_Feature_Vector.txt")
    file_a.append("102_4_Feature_Vector.txt")
    file_a.append("102_5_Feature_Vector.txt")
    file_a.append("102_6_Feature_Vector.txt")
    file_a.append("102_7_Feature_Vector.txt")
    file_a.append("102_8_Feature_Vector.txt")
    file_a.append("103_1_Feature_Vector.txt")
    file_a.append("103_2_Feature_Vector.txt")
    file_a.append("103_3_Feature_Vector.txt")
    file_a.append("103_4_Feature_Vector.txt")

    file_sa.append("101_1_Feature_Vector_series.txt")
    file_sa.append("101_2_Feature_Vector_series.txt")
    file_sa.append("101_3_Feature_Vector_series.txt")
    file_sa.append("101_4_Feature_Vector_series.txt")
    file_sa.append("101_5_Feature_Vector_series.txt")
    file_sa.append("101_6_Feature_Vector_series.txt")
    file_sa.append("101_7_Feature_Vector_series.txt")
    file_sa.append("101_8_Feature_Vector_series.txt")
    file_sa.append("102_1_Feature_Vector_series.txt")
    file_sa.append("102_2_Feature_Vector_series.txt")
    file_sa.append("102_3_Feature_Vector_series.txt")
    file_sa.append("102_4_Feature_Vector_series.txt")
    file_sa.append("102_5_Feature_Vector_series.txt")
    file_sa.append("102_6_Feature_Vector_series.txt")
    file_sa.append("102_7_Feature_Vector_series.txt")
    file_sa.append("102_8_Feature_Vector_series.txt")
    file_sa.append("103_1_Feature_Vector_series.txt")
    file_sa.append("103_2_Feature_Vector_series.txt")
    file_sa.append("103_3_Feature_Vector_series.txt")
    file_sa.append("103_4_Feature_Vector_series.txt")

    file_b.append("101_1_Point_Summary.txt")
    file_b.append("101_2_Point_Summary.txt")
    file_b.append("101_3_Point_Summary.txt")
    file_b.append("101_4_Point_Summary.txt")
    file_b.append("101_5_Point_Summary.txt")
    file_b.append("101_6_Point_Summary.txt")
    file_b.append("101_7_Point_Summary.txt")
    file_b.append("101_8_Point_Summary.txt")
    file_b.append("102_1_Point_Summary.txt")
    file_b.append("102_2_Point_Summary.txt")
    file_b.append("102_3_Point_Summary.txt")
    file_b.append("102_4_Point_Summary.txt")
    file_b.append("102_5_Point_Summary.txt")
    file_b.append("102_6_Point_Summary.txt")
    file_b.append("102_7_Point_Summary.txt")
    file_b.append("102_8_Point_Summary.txt")
    file_b.append("103_1_Point_Summary.txt")
    file_b.append("103_2_Point_Summary.txt")
    file_b.append("103_3_Point_Summary.txt")
    file_b.append("103_4_Point_Summary.txt")

    file_sb.append("101_1_Point_Summary_series.txt")
    file_sb.append("101_2_Point_Summary_series.txt")
    file_sb.append("101_3_Point_Summary_series.txt")
    file_sb.append("101_4_Point_Summary_series.txt")
    file_sb.append("101_5_Point_Summary_series.txt")
    file_sb.append("101_6_Point_Summary_series.txt")
    file_sb.append("101_7_Point_Summary_series.txt")
    file_sb.append("101_8_Point_Summary_series.txt")
    file_sb.append("102_1_Point_Summary_series.txt")
    file_sb.append("102_2_Point_Summary_series.txt")
    file_sb.append("102_3_Point_Summary_series.txt")
    file_sb.append("102_4_Point_Summary_series.txt")
    file_sb.append("102_5_Point_Summary_series.txt")
    file_sb.append("102_6_Point_Summary_series.txt")
    file_sb.append("102_7_Point_Summary_series.txt")
    file_sb.append("102_8_Point_Summary_series.txt")
    file_sb.append("103_1_Point_Summary_series.txt")
    file_sb.append("103_2_Point_Summary_series.txt")
    file_sb.append("103_3_Point_Summary_series.txt")
    file_sb.append("103_4_Point_Summary_series.txt")

    start1 = time.time()
    processes = []
    for i in range(20):
        processes.append(Process(target=crossing_number_algorithm1, args=(img[i], file_a[i], file_b[i],)))

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    stop1 = time.time()
    print("Parallel Execution Time is ", stop1 - start1)

    start2 = time.time()

    for i in range(20):
        crossing_number_algorithm2(img[i], file_sa[i], file_sb[i])

    stop2 = time.time()
    print("Sequential Execution Time is ", stop2 - start2)
    print("Completed")

