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


def is_valid_merge(color_dict, c1, c2):
    return True if (len(color_dict[c1])+len(color_dict[c2])) <= 4 else False


@wrapper_for_surrounding
def first_neighbours(mat, i2, j2, i, j):
    return 1 if mat[i2][j2] != 0 and mat[i][j] != 0 else 0


@wrapper_for_surrounding
def second_neighbours(mat, i2, j2, i, j):
    return first_neighbours(mat, i2, j2) if mat[i2][j2] != 0 and mat[i][j] != 0 else 0


@wrapper_for_surrounding
def third_neighbours(mat, i2, j2, i, j):
    return second_neighbours(mat, i2, j2) if mat[i2][j2] != 0 and mat[i][j] != 0 else 0


def valid_neighbours(mat, i, j, blacklist):
    bl = []
    valids = []
    if i != 0 and mat[i-1][j] != 0 and [i-1,j] not in bl:
        valids.append([i-1,j])
    if j != 0 and mat[i][j-1] != 0 and [i,j-1] not in bl:
        valids.append([i,j-1])
    if i != len(mat)-1:
        if mat[i+1][j] != 0 and [i+1,j] not in bl:
            valids.append([i+1,j])
    if j != len(mat)-1:
        if mat[i][j+1] != 0 and [i,j+1] not in bl:
            valids.append([i,j+1])
    return valids

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

    return cmpmat


if __name__ == '__main__':
    a = [[1,1,0,1],[1,1,0,0],[0,1,1,1],[0,0,1,1]]
    b = sol(a)
    c = [([0]*4) for i in range(4)]
    d = [([0]*4) for i in range(4)]
    for i in range(len(a)):
        for j in range(len(a)):
            c[i][j] = third_neighbours(a,i,j)
            d[i][j] = first_neighbours(a,i,j)
    [print(i) for i in b]
    print()
    [print(i) for i in c]
    print()
    [print(i) for i in d]
    print()
    print(valid_neighbours(b,3,1,[]))
