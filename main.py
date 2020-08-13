import pyglet
from pyglet import shapes

win = pyglet.window.Window(960, 540)

grid_batch = pyglet.graphics.Batch()
tile_batch = pyglet.graphics.Batch()

board_gen = []
grid_left = []
grid_right = []
tiles = []
divider = shapes.Line(480, 20, 480, 520, batch=grid_batch, color=(255,0,0))

grid_len = 10 #int(input('Grid length? '))
if grid_len < 4:
    grid_len = 4
increment = 400 / grid_len


def draw_grids(grid_length):
    """draws divider and grid backgrounds"""
    global grid_batch, grid_left, grid_right, increment
    for i in range(0,int(grid_length)+1):
        grid_left.append(shapes.Line(40+increment*i, 70, 40+increment*i, 470, batch=grid_batch))
        grid_right.append(shapes.Line(520+increment*i, 70, 520+increment*i, 470, batch=grid_batch))
        grid_left.append(shapes.Line(40, 70+increment*i, 440, 70+increment*i, batch=grid_batch))
        grid_right.append(shapes.Line(520, 70+increment*i, 920, 70+increment*i, batch=grid_batch))


""""@win.event()
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:"""


@win.event()
def on_draw():
    win.clear()
    tile_batch.draw()
    grid_batch.draw()



draw_grids(grid_len)
#a = input('wait')
pyglet.app.run()
