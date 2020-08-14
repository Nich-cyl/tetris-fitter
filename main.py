"""MAIN PROCESS"""

import pyglet
from pyglet.window import key
import generate
import display

win = pyglet.window.Window(960, 540)

grid_batch, tile_batch = pyglet.graphics.Batch(), pyglet.graphics.Batch()

board_gen, grid, tiles_left, tiles_right = [], [], [], []
grid_len = int(input('Grid length? '))


@win.event()
def on_key_press(symbol, modifiers):
    if symbol == key._1:
        global tiles_left
        tiles_left = display.draw_tiles(prb, tile_batch, True, True)
    elif symbol == key._2:
        global tiles_right
        tiles_right = display.draw_tiles(sol, tile_batch, False, False)


@win.event()
def on_draw():
    win.clear()
    tile_batch.draw()
    grid_batch.draw()


grid = display.draw_grids(grid_len, grid_batch)
[prb, sol] = generate.gen(grid_len)
#a = input('wait')
pyglet.app.run()
