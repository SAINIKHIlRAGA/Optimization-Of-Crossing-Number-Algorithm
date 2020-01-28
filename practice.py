from multiprocessing import Process, current_process
import os


def a():
    pid = os.getpid()
    pname = current_process().name
    print(f"{pname} says it's  ID is {pid}")


if __name__ == '__main__':
    processes = []
    for i in range(10):
        proc1 = Process(target=a)
        proc1.start()
        processes.append(proc1)
    for p in processes:
        p.join()
