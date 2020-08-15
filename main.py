"""MAIN PROCESS"""

import pyglet
from pyglet.window import key
import generate
import solve
import display

win = pyglet.window.Window(960, 540)

grid_batch, tile_batch = pyglet.graphics.Batch(), pyglet.graphics.Batch()

board_gen, tiles_left, tiles_right = [], [], []
grid_len = int(input('Grid length? '))


@win.event()
def on_key_press(symbol, modifiers):
    global tiles_left, tiles_right
    if symbol == key._0:
        tiles_left, tiles_right = [], []
    elif symbol == key._1:
        tiles_left = display.draw_tiles(prb, tile_batch, True, True)
    elif symbol == key._2:
        tiles_left = display.draw_tiles(sol, tile_batch, True, False)
    elif symbol == key._3:
        tiles_right = display.draw_tiles(cmp, tile_batch, False, False)


@win.event()
def on_draw():
    win.clear()
    tile_batch.draw()
    grid_batch.draw()


grid = display.draw_grids(grid_len, grid_batch)
[prb, sol] = generate.gen(grid_len)
#prb = [[1,1,1,0,0],[0,1,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
cmp = solve.sol(prb)
pyglet.app.run()
