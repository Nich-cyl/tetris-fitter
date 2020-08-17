"""GENERATES PROBLEM & SOLUTION BOARDS"""

import pyglet
from random import choice

"""(0,0) is in top left corner; +ve x = right; +ve y = down"""
I0 = ((1, 0), (2, 0), (3, 0))
I1 = ((0, 1), (0, 2), (0, 3))
O1 = ((0, 1), (1, 0), (1, 1))
T1 = ((1, 0), (2, 0), (1, 1))
T2 = ((0, 1), (0, 2), (-1, 1))  # -ve x -1,1
T3 = ((-1, 1), (0, 1), (1, 1))  # -ve x -1,1
T4 = ((0, 1), (0, 2), (1, 1))
L1 = ((1, 0), (2, 0), (0, 1))
L2 = ((1, 0), (1, 1), (1, 2))
L3 = ((1, 0), (2, 0), (2, -1))  # -ve y 2,-1
L4 = ((0, 1), (0, 2), (1, 2))
J1 = ((1, 0), (2, 0), (2, 1))
J2 = ((0, 1), (0, 2), (-1, 2))  # -ve x -1,2
J3 = ((0, 1), (1, 1), (2, 1))
J4 = ((1, 0), (0, 1), (0, 2))
Z1 = ((1, 0), (1, 1), (2, 1))
Z2 = ((1, 0), (1, -1), (0, 1))  # -ve y 1,-1
S1 = ((1, 0), (0, 1), (-1, 1))  # -ve x -1,1
S2 = ((0, 1), (1, 1), (1, 2))

blocks = [I0, I1, O1, T1, T2, T3, T4, L1, L2, L3, L4, J1, J2, J3, J4, Z1, Z2, S1, S2]


def gen(size):
    """fills grid length size with tetrominos. increase tried in while cond for fewer blanks."""
    prbmat = [([0] * size) for i in range(size)]
    solmat = [([0] * size) for i in range(size)]
    tile_no = 1
    for i in range(size):
        for j in range(size):
            if prbmat[i][j] == 0:
                tried = 0
                while tried <= 3:
                    test_block = choice(blocks)
                    try:
                        fit = True
                        for tile in test_block:
                            if (i + tile[0]) < 0 or (j + tile[1]) < 0:
                                raise IndexError
                            if prbmat[i + tile[0]][j + tile[1]] == 1:
                                fit = False
                                break
                        if fit:
                            prbmat[i][j] = 1
                            solmat[i][j] = tile_no
                            for tile in test_block:
                                prbmat[i + tile[0]][j + tile[1]] = 1
                                solmat[i + tile[0]][j + tile[1]] = tile_no
                            tried = 3
                            tile_no += 1
                    except IndexError:
                        pass
                    tried += 1
    return [prbmat, solmat]


if __name__ == '__main__':
    """generates & prints grid of desired length"""
    [prb, sol] = gen(10)
    [print(i) for i in prb]
    print()
    [print(i) for i in sol]
