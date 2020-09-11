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
    def function_wrapper(mat, i, j, blacklist, color_dict):
        holder = 0
        if i != 0: holder += func(mat, i - 1, j, i, j, blacklist, color_dict)
        if j != 0: holder += func(mat, i, j - 1, i, j, blacklist, color_dict)
        try:
            holder += func(mat, i + 1, j, i, j, blacklist, color_dict)
        except IndexError:
            pass
        try:
            holder += func(mat, i, j + 1, i, j, blacklist, color_dict)
        except IndexError:
            pass
        return holder
    return function_wrapper


@wrapper_for_each_in_grid
@wrapper_for_surrounding
def sum_surrounding(mat, i2, j2, i, j, blacklist, color_dict):
    return mat[i2][j2] if mat[i][j] != 0 else 0


def is_valid_merge(color_dict, c1, c2):
    return len(color_dict[c1])+len(color_dict[c2]) <= 4


@wrapper_for_surrounding
def first_neighbours(mat, i2, j2, i, j, blacklist, color_dict):
    c1, c2 = mat[i][j], mat[i2][j2]
    return 1 if c1 != 0 and c2 != 0 and c1 != c2 and [i2,j2] not in blacklist[i,j] and is_valid_merge(color_dict, c1, c2) else 0


@wrapper_for_surrounding
def second_neighbours(mat, i2, j2, i, j, blacklist, color_dict):
    c1, c2 = mat[i][j], mat[i2][j2]
    return first_neighbours(mat, i2, j2, blacklist, color_dict) if c1 != 0 and c2 != 0 and [i2,j2] not in blacklist[i,j] and is_valid_merge(color_dict, c1, c2) else 0


@wrapper_for_surrounding
def third_neighbours(mat, i2, j2, i, j, blacklist, color_dict):
    c1, c2 = mat[i][j], mat[i2][j2]
    return second_neighbours(mat, i2, j2, blacklist, color_dict) if c1 != 0 and c2 != 0 and [i2,j2] not in blacklist[i,j] and is_valid_merge(color_dict, c1, c2) else 0


def valid_neighbours(mat, i, j, blacklist, color_dict):
    bl = blacklist[i,j]
    valids = []
    if i != 0 and mat[i-1][j] != 0 and [i-1,j] not in bl and is_valid_merge(color_dict, mat[i][j], mat[i-1][j]):
        valids.append([i-1,j])
    if j != 0 and mat[i][j-1] != 0 and [i,j-1] not in bl and is_valid_merge(color_dict, mat[i][j], mat[i][j-1]):
        valids.append([i,j-1])
    if i != len(mat)-1:
        if mat[i+1][j] != 0 and [i+1,j] not in bl and is_valid_merge(color_dict, mat[i][j], mat[i+1][j]):
            valids.append([i+1,j])
    if j != len(mat)-1:
        if mat[i][j+1] != 0 and [i,j+1] not in bl and is_valid_merge(color_dict, mat[i][j], mat[i][j+1]):
            valids.append([i,j+1])
    return valids


def merge_colors(mat, color_dict, c1, c2):
    for t in color_dict[c2]:
        mat[t[0]][t[1]] = c1
        color_dict[c1].append(t)
    color_dict.pop(c2)


def loneliest(mat, i, j, blacklist, color_dict):
    valids = valid_neighbours(mat, i, j, blacklist, color_dict)
    firsts = [first_neighbours(mat, t[0], t[1], blacklist, color_dict) for t in valids]
    guess = False
    lonely = []
    if len(valids) > 0:
        if firsts.count(min(firsts)) == 1:
            for t in valids:
                if first_neighbours(mat, t[0], t[1], blacklist, color_dict) == min(firsts):
                    lonely = t
                    break
        else:
            seconds = [second_neighbours(mat, t[0], t[1], blacklist, color_dict) for t in valids]
            for t in valids:
                if second_neighbours(mat, t[0], t[1], blacklist, color_dict) == min(seconds):
                    lonely = t
                    if seconds.count(min(seconds)) != 1:
                        guess = True
                        break
    return [lonely, guess]


def check_tile(mat, i, j, color_dict, blacklist, log, threshold, can_guess):
    if first_neighbours(mat, i, j, blacklist, color_dict) <= threshold:
        [l, guess] = loneliest(mat, i, j, blacklist, color_dict)
        if l:
            c1, c2 = mat[i][j], mat[l[0]][l[1]]
            if guess == can_guess and c1 != c2:
                if guess:
                    log.insert(0,[[c2, color_dict[c2].copy(), [i,j], l.copy()]])
                else:
                    log[0].insert(0,[c2, color_dict[c2].copy()])
                merge_colors(mat, color_dict, c1, c2)
                blacklist[i,j].append(l)
                blacklist[l[0],l[1]].append([i,j])
                return 1
            else:
                return 0
        else:
            return 0
    else:
        return 0


def check_grid(mat, color_dict, blacklist, log, threshold, can_guess):
    """checks until can't guess anymore"""
    dim = len(mat)
    merged = 1
    while merged > 0:
        merged = 0
        for i in range(dim):
            for j in range(dim):
                if mat[i][j] != 0:
                    merged += check_tile(mat, i, j, color_dict, blacklist, log, threshold, can_guess)


def is_stuck(mat, color_dict, blacklist):
    for color in color_dict.keys():
        if len(color_dict[color]) != 4:
            valid_count = 0
            for t in color_dict[color]:
                valid_count += len(valid_neighbours(mat, t[0], t[1], blacklist, color_dict))
            if valid_count == 0:
                return True
    return False


def is_complete(mat, color_dict, blacklist):
    for color in color_dict.keys():
        if len(color_dict[color]) != 4:
            return False
    return True


def rollback(mat, color_dict, blacklist, log):
    while len(log[0]) > 0:
        color = log[0][0][0]
        color_dict[color] = []
        for t in log[0][0][1]:
            color_dict[mat[t[0]][t[1]]].remove(t)
            color_dict[color].append(t)
            mat[t[0]][t[1]] = color
        if len(log[0]) == 1:
            break
        log[0].pop(0)
    if len(log[0]) == 4:
        blacklist[tuple(log[0][0][3])].append(log[0][0][2])
        blacklist[tuple(log[0][0][2])].append(log[0][0][3])
    log.pop(0)


def sol(prbmat):
    dim = len(prbmat)
    cmpmat = [([0]*dim) for i in range(dim)]
    color_dict = {}
    blacklist = {}
    log = [[]]
    num = 1
    for i in range(dim):
        for j in range(dim):
            if prbmat[i][j] == 1:
                cmpmat[i][j] = num
                color_dict[num] = [[i,j]]
                num += 1
            else:
                cmpmat[i][j] = 0
            blacklist[i, j] = []
    check_grid(cmpmat, color_dict, blacklist, log, 1, False)
    """TESTING"""
    check_grid(cmpmat, color_dict, blacklist, log, 2, False)
    check_grid(cmpmat, color_dict, blacklist, log, 2, True)
    check_grid(cmpmat, color_dict, blacklist, log, 2, False)
    check_grid(cmpmat, color_dict, blacklist, log, 1, False)
    [print(i) for c in log for i in c]
    print()
    [print(i) for i in cmpmat]
    print()
    rollback(cmpmat, color_dict, blacklist, log)
    [print(i) for i in cmpmat]
    print()
    rollback(cmpmat, color_dict, blacklist, log)
    [print(i) for i in cmpmat]
    return cmpmat


if __name__ == '__main__':
    a = [[1,1,0,1],
         [0,1,1,1],
         [0,1,1,1],
         [0,1,1,1]]
    b = sol(a)
    print()
    [print(i) for i in b]
    print()

