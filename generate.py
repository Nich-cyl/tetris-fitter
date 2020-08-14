"""GENERATES PROBLEM & SOLUTION BOARDS"""

import pyglet
from random import randrange

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

blocks = {1: T2, 2: T3, 3: J2, 4: S1,  # -ve x
          14: I0, 15: I1, 16: O1, 17: T1, 5: T4, 6: L1, 7: L2, 8: L4, 9: J1, 10: J3, 11: J4, 12: Z1, 13: S2,
          18: L3, 19: Z2}  # -ve y


def print_block(entry_no, origin, increment, holding_arr, batch):
    """prints block.. ig"""
    global blocks
    holding_arr.append(pyglet.shapes.Rectangle(origin[0],
                                               origin[1],
                                               increment, increment,
                                               color=(0, 0, 255),
                                               batch=batch))
    for tile in blocks[entry_no]:
        holding_arr.append(pyglet.shapes.Rectangle(origin[0] + tile[0] * increment,
                                                   origin[1] - tile[1] * increment,
                                                   increment, increment,
                                                   color=(0, 0, 255),
                                                   batch=batch))


def gen(size):
    """fills grid length size with tetrominos. increase tried in while cond for fewer blanks."""
    prbmat = [([0] * size) for i in range(size)]
    solmat = [([0] * size) for i in range(size)]
    tile_no = 1
    for i in range(size):
        for j in range(size):
            if prbmat[i][j] == 0:
                tried = 0
                while tried <= 1:
                    index = randrange(1, 20)
                    test_block = blocks[index]
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
                        print('Block out of range. Oh well.')
                    tried += 1
    return [prbmat, solmat]


if __name__ == '__main__':
    """generates & prints grid of desired length"""
    [prb, sol] = gen(10)
    [print(i) for i in prb]
    print()
    [print(i) for i in sol]
