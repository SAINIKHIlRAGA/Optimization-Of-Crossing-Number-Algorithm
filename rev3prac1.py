import numpy as np
from multiprocessing import Pool


def fun(x, y, z):


    return 1


def fun_wrapper(indices):
    fun(*indices)


if __name__ == '__main__':
    dim1 = 10
    dim2 = 20
    dim3 = 30

    result = np.zeros([dim1, dim2, dim3])

    pool = Pool(processes=8)
    for i in range(dim1):
        for j in range(dim2):
            result[i, j] = pool.map(fun_wrapper, [(i, j, k) for k in range(dim3)])
    print(result)