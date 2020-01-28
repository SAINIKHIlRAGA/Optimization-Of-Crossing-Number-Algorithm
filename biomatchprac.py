from ast import literal_eval
from multiprocessing import Process
import time
import math


def matching(file_a, file):
    max = 0
    for j in range(1, 2):
        if file_a != file[j]:
            matched = match(file_a, file[j])
            if matched > max:
                max = matched
                matched_file = file[j]
    # print("Matching FingerPrint for ", file_a, "is ", matched_file, " with ", max, " matches")


def match(file_a, file_b):
    collection1 = []
    collection2 = []
    collection3 = []
    collection4 = []
    with open(file_a, "r") as f:
        collection1.append(f.read().splitlines())
    f.close()
    with open(file_b, "r") as f:
        collection2.append(f.read().splitlines())
    f.close()
    for i in collection1:
        for j in i:
            k = literal_eval(j)
            if k['type'] == 'valid_bifurcation_point':
                collection3.append(k)
    for i in collection2:
        for j in i:
            k = literal_eval(j)
            if k['type'] == 'valid_bifurcation_point':
                collection4.append(k)

    min_dict_1 = {}
    min_dict_2 = {}
    for i in range(collection3.__len__()):
        min = 1000000000
        for j in range(collection3.__len__()):
            if j != i:
                x = collection3[i]['position_x']-collection3[j]['position_x']
                x *= x
                y = collection3[i]['position_y'] - collection3[j]['position_y']
                y *= y
                dist = math.sqrt(x+y)
                if dist < min:
                    min = dist
        min_dict_1[i] = min
    print(min_dict_1)
    for i in min_dict_1.keys():
        for j in min_dict_2.keys():
            if min_dict_1[i] == min_dict_2[j]:
                print(i, "--------------", j)
    for i in range(collection4.__len__()):
        min = 1000000000
        for j in range(collection4.__len__()):
            if j != i:
                x = collection4[i]['position_x']-collection4[j]['position_x']
                x *= x
                y = collection4[i]['position_y'] - collection4[j]['position_y']
                y *= y
                dist = math.sqrt(x+y)
                if dist < min:
                    min = dist
        min_dict_2[i] = min
    print(min_dict_2)
    matched = 0
    k = []
    for i in collection3:
        for j in collection4:
            if j not in k:
                if i['orientation'] == j['orientation']:
                    matched += 1
                    k.append(j)
                    break
    return matched


if __name__ == '__main__':
    file_a = list()
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

    start1 = time.time()
    processes = []
    for i in range(1):
        processes.append(Process(target=matching, args=(file_a[i], file_a,)))

    for process in processes:
        process.start()
    for process in processes:
        process.join()
    stop1 = time.time()
    # start2 = time.time()
    # for i in range(20):
    #     for j in range(1, 20):
    #         if j != i:
    #             match(file_a[i], file_a[j])
    # stop2 = time.time()
    # print("Parallel Execution Time is ", stop1 - start1)
    # print("Sequential Execution Time is ", stop2 - start2)
    # print("Completed")
    #
