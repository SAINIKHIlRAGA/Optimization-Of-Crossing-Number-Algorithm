from ast import literal_eval
from multiprocessing import Process
import time
import threading

collection1 = []
collection2 = []
collection3 = []
collection4 = []


def matching(file_a, file):
    max = 0
    for j in range(1, 20):
        if file_a != file[j]:
            matched = match(file_a, file[j])
            if matched > max:
                max = matched
                matched_file = file[j]
    print("Matching FingerPrint for ", file_a, "is ", matched_file, " with ", max, " matches")


def read_file1(file):
    global collection1
    with open(file, "r") as f:
        collection1.append(f.read().splitlines())
    f.close()


def read_file2(file):
    global collection2
    with open(file, "r") as f:
        collection2.append(f.read().splitlines())
    f.close()

def extract_valid_points_1():
    global collection3
    for i in collection1:
        for j in i:
            k = literal_eval(j)
            if k['type'] == 'valid_bifurcation_point':
                collection3.append(k)


def extract_valid_points_2():
    global collection4
    for i in collection2:
        for j in i:
            k = literal_eval(j)
            if k['type'] == 'valid_bifurcation_point':
                collection4.append(k)


def match(file_a, file_b):
    threads1 = list()
    threads1.append(threading.Thread(target=read_file1, args=(file_a,)))
    threads1.append(threading.Thread(target=read_file2, args=(file_b,)))
    print("OK1")
    for thread in threads1:
        thread.start()
    for thread in threads1:
        thread.join()
        print("OK2")
    threads2 = list()
    threads2.append(threading.Thread(target=extract_valid_points_1, args=()))
    threads2.append(threading.Thread(target=extract_valid_points_2, args=()))
    for thread in threads2:
        thread.start()
    for thread in threads2:
        thread.join()
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
    for i in range(20):
        processes.append(Process(target=matching, args=(file_a[i], file_a,)))

    for process in processes:
        process.start()
    for process in processes:
        process.join()
    stop1 = time.time()
    start2 = time.time()
    for i in range(20):
        for j in range(1, 20):
            if j != i:
                match(file_a[i], file_a[j])
    stop2 = time.time()
    print("Parallel Execution Time is ", stop1 - start1)
    print("Sequential Execution Time is ", stop2 - start2)
    print("Completed")

