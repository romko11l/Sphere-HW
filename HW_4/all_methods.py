import cProfile
import pstats
import numpy as np
from memory_profiler import profile


"""Self-written fast version of the calculation"""


def mat_mul(matr1: list, matr2: list) -> list:
    """Multiplication of two matrices 2 * 2"""
    a11 = matr1[0][0] * matr2[0][0] + matr1[0][1] * matr2[1][0]
    a12 = matr1[0][0] * matr2[0][1] + matr1[0][1] * matr2[1][1]
    a21 = matr1[1][0] * matr2[0][0] + matr1[1][1] * matr2[1][0]
    a22 = matr1[1][0] * matr2[0][1] + matr1[1][1] * matr2[1][1]
    return [[a11, a12], [a21, a22]]


def self_written_calc(n: int) -> int:
    """Calculating n fibonacci number"""
    if n == 2:
        return 2
    if n == 1:
        return 1
    n -= 2
    matr = [[0, 1], [1, 1]]
    matr_list = [[[0, 1], [1, 1]]]
    decomposition = bin(n)
    while n > 0:
        if n == 1:
            matr_list = matr_list[::-1]
            matr = [[0, 1], [1, 1]]
            for i in range(2, len(decomposition)):
                if decomposition[i] == str(1):
                    matr = mat_mul(matr, matr_list[i-2])
            return matr[1][0] + matr[1][1]
        matr = mat_mul(matr, matr)
        matr_list.append(matr)
        n = n // 2


"""Numpy fast version of the calculation"""

MATRIX = np.array([[0, 1], [1, 1]])
START = np.array([1, 1])


def numpy_calc(n: int) -> int:
    """Calculating n fibonacci number"""
    if n == 1:
        return 1
    if n == 2:
        return 2
    res = np.linalg.matrix_power(MATRIX, n-1)
    return START.dot(res)[1]


"""Slow version of the calculation"""


def slow_calc(n: int) -> int:
    """Calculating n fibonacci number"""
    if n > 2:
        return slow_calc(n-1) + slow_calc(n-2)
    if n == 2:
        return 2
    if n == 1:
        return 1
    return None


if __name__ == '__main__':
    self_written_calc(3)
    i = 1
    while True:
        if numpy_calc(i) != self_written_calc(i):
            print(numpy_calc(i))
            print(self_written_calc(i))
            print(i)
            break
        i += 1
    """
    profiler = cProfile.Profile()
    profiler.enable()
    slow_calc(25)
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('ncalls')
    stats.print_stats()
    """
