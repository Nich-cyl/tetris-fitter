"""MAIN PROCESS"""

import pyglet
from pyglet.window import key
import generate
import display
import solve

win = pyglet.window.Window(960, 540)

grid_batch, tile_batch = pyglet.graphics.Batch(), pyglet.graphics.Batch()

board_gen, grid, tiles_left, tiles_right = [], [], [], []
prb, sol, cmp = [], [], []
grid_len = int(input('Grid length? '))


@win.event()
def on_key_press(symbol, modifiers):
    global tiles_left, tiles_right, prb, sol, cmp, grid
    if symbol == key._0:
        tiles_left, tiles_right = [], []
        [prb, sol] = generate.gen(grid_len)
    elif symbol == key._1:
        tiles_left = display.draw_tiles(prb, tile_batch, True, True)
    elif symbol == key._2:
        tiles_left = display.draw_tiles(sol, tile_batch, True, False)
    elif symbol == key._3:
        cmp = solve.sol(prb)
        tiles_right = display.draw_tiles(cmp, tile_batch, False, False)
        print('done')


@win.event()
def on_draw():
    win.clear()
    tile_batch.draw()
    grid_batch.draw()


grid = display.draw_grids(grid_len, grid_batch)
[prb, sol] = generate.gen(grid_len)
#a = input('wait')
pyglet.app.run()
