from multiprocessing import Pool
import time


def sum_square(num):
    sum = 0
    for i in range(num):
        sum += i*i
    return sum


def sum_squares_mp(nums):
    x = time.time()
    p = Pool()
    res = p.map(sum_square, nums)
    y = time.time()
    p.close()
    p.join()
    print("Parallel Execution Time is ", y - x)


def sum_squares_no_mp(nums):
    x = time.time()
    result = []
    for i in nums:
        result.append(sum_square(i))
    y = time.time()
    print("Serial Execution Time is ", y - x)


if __name__ == '__main__':
    nums = range(10000)
    sum_squares_mp(nums)
    sum_squares_no_mp(nums)

