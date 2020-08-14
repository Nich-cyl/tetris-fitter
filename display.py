from pyglet import shapes

def draw_grids(grid_length, batch):
    """draws divider and grid backgrounds"""
    increment = 400 / grid_length
    holder = [shapes.Line(480, 20, 480, 520, batch=batch, color=(255,0,0))]
    for i in range(0,int(grid_length)+1):
        holder.append(shapes.Line(40+increment*i, 70, 40+increment*i, 470, batch=batch))
        holder.append(shapes.Line(520+increment*i, 70, 520+increment*i, 470, batch=batch))
        holder.append(shapes.Line(40, 70+increment*i, 440, 70+increment*i, batch=batch))
        holder.append(shapes.Line(520, 70+increment*i, 920, 70+increment*i, batch=batch))
    return holder
