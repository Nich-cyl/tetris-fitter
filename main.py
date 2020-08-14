import pyglet
from pyglet import shapes
import generate
import display

win = pyglet.window.Window(960, 540)

grid_batch = pyglet.graphics.Batch()
tile_batch = pyglet.graphics.Batch()

board_gen = []
grid = []
tiles = []
grid_len = 10 #int(input('Grid length? '))


""""@win.event()
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:"""


@win.event()
def on_draw():
    win.clear()
    tile_batch.draw()
    grid_batch.draw()


#generate.print_block(1,(200,430),increment,tiles,tile_batch)
grid = display.draw_grids(grid_len, grid_batch)
#a = input('wait')
pyglet.app.run()
