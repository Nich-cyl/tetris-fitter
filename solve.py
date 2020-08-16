"""SOLVES PROBLEM BOARDS"""

from itertools import count

def is_complete(cmp_extended, color):
    """returns true if tetromino has 4 tiles"""
    return {c: cmp_extended.count(c) for c in cmp_extended}[color] == 4


def is_valid_merge(cmp_extended, color1, color2):
    """returns true if addition of colour groups do not result in invalid tetromino"""
    freq_dict = {c: cmp_extended.count(c) for c in cmp_extended}
    return freq_dict[color1] + freq_dict[color2] <= 4


def return_neighbours(prbmat, i, j):
    """returns number of nonzero neighbours, given tile is nonzero"""
    holder = 0
    if i != 0: holder += 1 if prbmat[i-1][j] != 0 else 0
    if j != 0: holder += 1 if prbmat[i][j-1] != 0 else 0
    try:
        holder += 1 if prbmat[i+1][j] != 0 else 0
    except IndexError:
        pass
    try:
        holder += 1 if prbmat[i][j+1] != 0 else 0
    except IndexError:
        pass
    return holder if prbmat[i][j] != 0 else 0


def get_neighbours(neighbour_count, i, j):
    holder = []
    if i != 0 and neighbour_count[i-1][j] != 0: holder.append([i-1,j])
    if j != 0 and neighbour_count[i][j-1] != 0: holder.append([i,j-1])
    for tile in [[i+1,j],[i,j+1]]:
        try:
            if neighbour_count[tile[0]][tile[1]] != 0: holder.append([tile[0],tile[1]])
        except IndexError:
            pass
    return holder


def return_neighbours_of_neighbours(neighbour_count, i, j):
    """returns no. of neighbours of neighbours. some duplicates but fine since only for comparison purposes"""
    holder = 0
    if i != 0 and neighbour_count[i-1][j] != 0: holder += neighbour_count[i-1][j] - 1
    if j != 0 and neighbour_count[i][j-1] != 0: holder += neighbour_count[i][j-1] - 1
    for tile in [[i+1,j],[i,j+1]]:
        try:
            if neighbour_count[tile[0]][tile[1]] != 0: holder += neighbour_count[tile[0]][tile[1]] - 1
        except IndexError:
            pass
    return holder


def update_neighbours_of_neighbours(cmpmat, neighbour_count, i, j):
    """triggers updating of neighbour count of neighbouring tiles if is not of same colour"""
    if i != 0 and cmpmat[i][j] != cmpmat[i - 1][j]:
        neighbour_count[i - 1][j] = return_neighbours(neighbour_count, i - 1, j)
    if j != 0 and cmpmat[i][j] != cmpmat[i][j - 1]:
        neighbour_count[i][j - 1] = return_neighbours(neighbour_count, i, j - 1)
    try:
        if cmpmat[i][j] != cmpmat[i + 1][j]: neighbour_count[i + 1][j] = return_neighbours(neighbour_count, i + 1, j)
    except IndexError:
        pass
    try:
        if cmpmat[i][j] != cmpmat[i][j + 1]: neighbour_count[i][j + 1] = return_neighbours(neighbour_count, i, j + 1)
    except IndexError:
        pass


def fewer_neighbours(neighbour_count, i1, j1, i2, j2):
    """returns less connected neighbour for choice between tiles (i1,j1) or (i2,j2)"""
    if neighbour_count[i1][j1] != neighbour_count[i2][j2]:
        return [i1,j1] if neighbour_count[i1][j1] < neighbour_count[i2][j2] else [i2][j2]
    else:
        tile1_neighbour2 = return_neighbours_of_neighbours(neighbour_count, i1, j1)
        tile2_neighbour2 = return_neighbours_of_neighbours(neighbour_count, i2, j2)
        if tile1_neighbour2 == tile2_neighbour2:
            return None
        else:
            return [i1,j1] if tile1_neighbour2 < tile2_neighbour2 else [i2,j2]


def merge_colors(cmpmat, i, j, x, y, arr):
    """merges two colour groups"""
    if [i,j] not in arr: arr.append([i,j])
    if [x,y] not in arr:
        if x != 0 and cmpmat[x-1][y] == cmpmat[x][y] and [x-1, y] not in arr:
            arr.append([x, y])
            merge_colors(cmpmat, i, j, x-1, y, arr)
        if y != 0 and cmpmat[x][y-1] == cmpmat[x][y] and [x, y-1] not in arr:
            arr.append([x, y])
            merge_colors(cmpmat, i, j, x, y-1, arr)
        try:
            if cmpmat[x+1][y] == cmpmat[x][y] and [x+1, y] not in arr:
                arr.append([x, y])
                merge_colors(cmpmat, i, j, x+1, y, arr)
        except IndexError:
            pass
        try:
            if cmpmat[x][y+1] == cmpmat[x][y] and [x, y+1] not in arr:
                arr.append([x, y])
                merge_colors(cmpmat, i, j, x, y+1, arr)
        except IndexError:
            pass
    cmpmat[x][y] = cmpmat[i][j]


def merge(cmpmat, neighbour_count, i, j, x, y):
    neighbour_count[x][y] -= 1
    neighbour_count[i][j] -= 1
    merge_colors(cmpmat, i, j, x, y, [])
    if is_complete([a for b in cmpmat for a in b], cmpmat[i][j]):
        neighbour_count[x][y] = 0
        update_neighbours_of_neighbours(cmpmat, neighbour_count, x, y)


def link_ones(cmpmat, neighbour_count):
    """attaches ones to neighbouring tile if is valid"""
    size = len(neighbour_count)
    for i in range(size):
        for j in range(size):
            if neighbour_count[i][j] == 1 and not is_complete([a for b in cmpmat for a in b], cmpmat[i][j]):
                """debug printing"""
                a = [print(i) for i in neighbour_count]
                print()
                a = [print(i) for i in cmpmat]
                print("\n\n")

                if i != 0 and neighbour_count[i-1][j] != 0: x, y = i-1, j
                elif j != 0 and neighbour_count[i][j-1] != 0: x, y = i, j-1
                else:
                    try:
                        if neighbour_count[i+1][j] != 0: x, y = i+1, j
                    except IndexError:
                        pass
                    try:
                        if neighbour_count[i][j+1] != 0: x, y = i, j+1
                    except IndexError:
                        pass
                if is_valid_merge([a for b in cmpmat for a in b], cmpmat[x][y], cmpmat[i][j]):
                    merge(cmpmat, neighbour_count, i, j, x, y)


def link_twos(cmpmat, neighbour_count):
    size = len(neighbour_count)
    for i in range(size):
        for j in range(size):
            if neighbour_count[i][j] == 2 and not is_complete([a for b in cmpmat for a in b], cmpmat[i][j]):
                n_coords = get_neighbours(neighbour_count, i, j)
                lonelier = fewer_neighbours(neighbour_count,n_coords[0][0],n_coords[0][1],n_coords[1][0],n_coords[1][1])
                if lonelier is not None:
                    x, y = lonelier[0], lonelier[1]
                    if is_valid_merge([a for b in cmpmat for a in b], cmpmat[x][y], cmpmat[i][j]):
                        merge(cmpmat, neighbour_count, i, j, x, y)
                        link_ones(cmpmat, neighbour_count)


def sol(prbmat):
    """solves problem board. returns solved group board."""
    size = len(prbmat)
    cmpmat = [([0] * size) for i in range(size)]
    neighbour_count = [([0] * size) for i in range(size)]
    counter_gen = count(1)
    for i in range(size):
        for j in range(size):
            if prbmat[i][j] == 1:
                cmpmat[i][j] = next(counter_gen)
                neighbour_count[i][j] = return_neighbours(prbmat, i, j)
    while 1 in [item for sublist in neighbour_count for item in sublist]:
        link_ones(cmpmat, neighbour_count)
    #for a in range(20):
        #link_twos(cmpmat, neighbour_count)

    """debug printing"""
    a = [print(i) for i in neighbour_count]
    print()
    a = [print(i) for i in cmpmat]
    print("\n\n")
    return cmpmat


if __name__ == '__main__':
    prb = [[1,1,1,1],[1,1,0,0],[1,1,0,0],[0,1,0,0]]
    size = len(prb)
    cmp = [([0] * size) for i in range(size)]
    neighbour_count = [([0] * size) for i in range(size)]
    counter_gen = count(1)
    for i in range(size):
        for j in range(size):
            if prb[i][j] == 1:
                cmp[i][j] = next(counter_gen)
                neighbour_count[i][j] = return_neighbours(prb, i, j)
    print(fewer_neighbours(cmp, neighbour_count, 2, 1, 1, 1))
