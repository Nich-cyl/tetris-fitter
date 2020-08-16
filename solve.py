"""SOLVES PROBLEM GRIDS"""

def wrapper_for_each_in_grid(func):
    """runs func for all tiles, returning grid of outputs"""
    """applied func should take (mat, self_i, self_j, args)"""
    def function_wrapper(mat, *args):
        holder = [([0]*len(mat)) for a in range(len(mat))]
        for i in range(len(mat)):
            for j in range(len(mat)):
                holder[i][j] = func(mat, i, j, args)
        return holder
    return function_wrapper


def wrapper_for_surrounding(func):
    """runs func for neighbouring tiles, returning summing outputs in holder"""
    """applied func should take (mat, neighbour_i, neighbour_j, self_i, self_j, holder, args)"""
    def function_wrapper(mat, i, j, *args):
        holder = 0
        if i != 0: holder = func(mat, i - 1, j, i, j, holder, args)
        if j != 0: holder = func(mat, i, j - 1, i, j, holder, args)
        try:
            holder = func(mat, i + 1, j, i, j, holder, args)
        except IndexError:
            pass
        try:
            holder = func(mat, i, j + 1, i, j, holder, args)
        except IndexError:
            pass
        return holder
    return function_wrapper


def valid_neighbours(mat, i, j):
    if mat[i][j] == 0: return []
    valids = []
    if i != 0 and mat[i-1][j] != 0: valids.append([i - 1, j])
    if j != 0 and mat[i][j-1] != 0: valids.append([i, j - 1])
    if i != len(mat) - 1:
        if mat[i+1][j] != 0: valids.append([i + 1, j])
    if j != len(mat) - 1:
        if mat[i][j+1] != 0: valids.append([i, j + 1])
    return valids


@wrapper_for_each_in_grid
@wrapper_for_surrounding
def sum_surrounding(mat, i2, j2, i, j, holder, args):
    """sums surrounding if self is non-zero"""
    """takes (mat)"""
    return holder + (mat[i2][j2] if mat[i][j] != 0 else 0)


@wrapper_for_each_in_grid
@wrapper_for_surrounding
def neighbour_count(mat, i2, j2, i, j, holder, args):
    """gives number of non-zero neighbours"""
    """takes (mat)"""
    return holder + (1 if mat[i][j] != 0 and mat[i2][j2] != 0 else 0)


@wrapper_for_each_in_grid
def assign_colors(mat, i, j, args):
    """gives each non-zero a unique number"""
    """takes (mat, counter_gen)"""
    counter = args[0]
    return next(counter) if mat[i][j] != 0 else 0


def is_valid_merge(mat, color1, color2):
    """gives true if merged group tile number <= 4, else false"""
    mat_extended = [item for sublist in mat for item in sublist]
    return True if mat_extended.count(color1) + mat_extended.count(color2) <= 4 else False


def update_prox(mat):
    """gives 'connectivity' of each tile, prox1 shows neighbouring tiles"""
    prox1 = neighbour_count(mat)
    prox2 = sum_surrounding(prox1)
    prox3 = sum_surrounding(prox2)
    return [prox1, prox2, prox3]


def choose_loneliest(mat, i, j, prox1, prox2, prox3):
    if mat[i][j] == 0:
        return None
    valids = valid_neighbours(mat, i, j)
    prox1s = [prox1[t[0]][t[1]] for t in valids]
    if prox1s.count(min(prox1s)) == 1:
        return {prox1[t[0]][t[1]]:t for t in valids}[min(prox1s)]
    else:
        prox2s = [prox2[t[0]][t[1]] for t in valids]
        if prox2s.count(min(prox2s)) == 1:
            return {prox2[t[0]][t[1]]: t for t in valids}[min(prox2s)]
        else:
            prox3s = [prox3[t[0]][t[1]] for t in valids]
            if prox3s.count(min(prox3s)) == 1:
                return {prox3[t[0]][t[1]]: t for t in valids}[min(prox3s)]
            else:
                return None

def sol(prbmat):
    """groups tiles in 4s"""
    cmpmat = assign_colors(prbmat, (a for a in range(1, len(prbmat) ** 2 + 1)))
    [prox1, prox2, prox3] = update_prox(prbmat)
    return cmpmat


if __name__ == '__main__':
    """testing"""
    a = [[1,1,1,0],[1,1,0,1],[1,1,1,1],[1,0,0,1]]
    [b, c, d] = update_prox(a)
    e = sol(a)
    [print(i) for i in a]
    print()
    [print(i) for i in b]
    print()
    [print(i) for i in c]
    print()
    [print(i) for i in d]
    print()
    [print(i) for i in e]
    print()

    print(is_valid_merge([[1,1,0],[2,0,0],[0,0,0]], 1, 2))
    print()
    [print(i) for i in a]
    print()
    [print(f'{i}, {j}: {choose_loneliest(a,i,j,b,c,d)}') for i in range(4) for j in range(4)]
