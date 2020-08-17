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
    return holder + (1 if mat[i][j] != 0 and mat[i2][j2] != 0 and mat[i][j] != mat[i2][j2] else 0)


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


@wrapper_for_each_in_grid
def merge_colors_inner(mat, i, j, colors):
    """takes (mat, color1, color2), returns corrected mat w/ color2s replaced by color1s"""
    return colors[0] if mat[i][j] == colors[1] else mat[i][j]


def merge_colors(prbmat, cmpmat, color1, color2):
    """merges two colour groups. returns corrected prbmat & cmpmat"""
    prbmat = merge_colors_inner(prbmat, color1, color2)
    prbmat_extended = [item for sublist in prbmat for item in sublist]
    color2_coords = [[i, j] for i in range(len(prbmat)) for j in range(len(prbmat)) if prbmat[i][j] == color2]
    for tile in color2_coords:
        prbmat[tile[0]][tile[1]] = color1
    if prbmat_extended.count(color1) == 4:
        color1_coords = [[i,j] for i in range(len(prbmat)) for j in range(len(prbmat)) if prbmat[i][j] == color1]
        for tile in color1_coords:
            prbmat[tile[0]][tile[1]] = 0
            cmpmat[tile[0]][tile[1]] = color1
    return [prbmat, cmpmat]


def update_prox(mat):
    """returns 'connectivity' of each tile, prox1 shows neighbouring tiles"""
    prox1 = neighbour_count(mat)
    prox2 = sum_surrounding(prox1)
    prox3 = sum_surrounding(prox2)
    return [prox1, prox2, prox3]


def choose_loneliest(prbmat, i, j, prox1, prox2, prox3):
    """returns least 'connected' neighbour of tile, or None if all equally connected"""
    if prbmat[i][j] == 0:
        return None
    valids = valid_neighbours(prbmat, i, j)
    prox1s = [prox1[t[0]][t[1]] for t in valids if prbmat[t[0]][t[1]] != prbmat[i][j]]
    if prox1s.count(min(prox1s)) == 1:
        return {prox1[t[0]][t[1]]:t for t in valids if prbmat[t[0]][t[1]] != prbmat[i][j]}[min(prox1s)]
    else:
        prox2s = [prox2[t[0]][t[1]] for t in valids if prbmat[t[0]][t[1]] != prbmat[i][j]]
        if prox2s.count(min(prox2s)) == 1:
            return {prox2[t[0]][t[1]]: t for t in valids if prbmat[t[0]][t[1]] != prbmat[i][j]}[min(prox2s)]
        else:
            prox3s = [prox3[t[0]][t[1]] for t in valids if prbmat[t[0]][t[1]] != prbmat[i][j]]
            if prox3s.count(min(prox3s)) == 1:
                return {prox3[t[0]][t[1]]: t for t in valids if prbmat[t[0]][t[1]] != prbmat[i][j]}[min(prox3s)]
            else:
                return None


def link_1s(prbmat, cmpmat):
    [prox1, prox2, prox3] = update_prox(prbmat)
    while 1 in [item for sublist in prox1 for item in sublist]:
        for i1 in range(len(prbmat)):
            for j1 in range(len(prbmat)):
                if prox1[i1][j1] == 1:
                    [i2, j2] = choose_loneliest(prbmat, i1, j1, prox1, prox2, prox3)
                    color1, color2 = prbmat[i1][j1], prbmat[i2][j2]
                    if is_valid_merge(prbmat, color1, color2):
                        [prbmat, cmpmat] = merge_colors(prbmat, cmpmat, color1, color2)
                        [prox1, prox2, prox3] = update_prox(prbmat)
    return [prbmat, cmpmat]


def sol(prbmat):
    """groups tiles in 4s"""
    prbmat = assign_colors(prbmat, (a for a in range(1, len(prbmat) ** 2 + 1)))
    cmpmat = [([0] * len(prbmat)) for a in range(len(prbmat))]
    [prbmat, cmpmat] = link_1s(prbmat, cmpmat)
    return cmpmat


if __name__ == '__main__':
    """testing"""
    prb = [[1,1,1,0],
           [1,0,1,0],
           [1,0,0,0],
           [1,1,0,0]]
    [print(i) for i in prb]
    print()
    sol = sol(prb)
    [print(i) for i in sol]
