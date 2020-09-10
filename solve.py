"""SOLVES PROBLEM GRIDS"""

def color_gen(seed):
    return [(7*seed) % 256, (11*seed+50) % 256, (19*seed+100) % 256]


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

def sol(prbmat):
    dim = len(prbmat)
    cmpmat = [([0]*dim) for i in range(dim)]
    color_dict = {}
    num = 1
    for i in range(dim):
        for j in range(dim):
            if prbmat[i][j] == 1:
                cmpmat[i][j] = num
                color_dict[num] = [i,j]
                num += 1
            else:
                cmpmat[i][j] = 0
    print(color_dict)
    return cmpmat


if __name__ == '__main__':
    a = [[1,1,0],[1,0,0],[0,1,1]]
    b = sol(a)
    [print(i) for i in b]
