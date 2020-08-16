"""SOLVES PROBLEM GRIDS"""

def wrapper_for_each_in_grid(func):
    """runs func for all tiles, returning grid of outputs"""
    def function_wrapper(mat):
        holder = [([0]*len(mat)) for a in range(len(mat))]
        for i in range(len(mat)):
            for j in range(len(mat)):
                holder[i][j] = func(mat,i,j)
        return holder
    return function_wrapper


def wrapper_for_surrounding(func):
    """runs func for neighbouring tiles, returning summing outputs in holder"""
    def function_wrapper(mat, i, j):
        holder = 0
        if i != 0: holder += func(mat, i - 1, j, i, j)
        if j != 0: holder += func(mat, i, j - 1, i, j)
        try:
            holder += func(mat, i + 1, j, i, j)
        except IndexError:
            pass
        try:
            holder += func(mat, i, j + 1, i, j)
        except IndexError:
            pass
        return holder
    return function_wrapper


@wrapper_for_each_in_grid
@wrapper_for_surrounding
def sum_surrounding(mat, i2, j2, i, j):
    return mat[i2][j2] if mat[i][j] != 0 else 0
