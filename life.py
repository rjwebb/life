from repoze.lru import lru_cache
import itertools
import numpy as np
import random

three_bar = [
    (0,-1),
    (0,0),
    (0,1)
]


def probably(p):
    if p != None:
        return random.random() < p
    else:
        return False

def get_neighbours(x, y, shape):
    width, height = shape
    cells = []
    if x > 0:
        if y > 0:
            cells.append( (x-1, y-1) )
        if y < height - 1:
            cells.append( (x-1, y+1) )
        cells.append( (x-1, y) )

    if x < width - 1:
        # x + 1
        if y > 0:
            cells.append( (x+1, y-1) )
        if y < height - 1:
            cells.append( (x+1, y+1) )
        cells.append( (x+1, y) )

    if y > 0:
        cells.append( (x, y-1) )
    if y < height - 1:
        cells.append( (x, y+1) )

    return cells


def add_to_grid(grid, thing, x, y):
    """
    thing is a list of relative coordinates
    for every point in thing relative to (x,y), set the corresponding bit in grid to 1
    """
    for c_x, c_y in thing:
        grid[x+c_x, y+c_y] = 1

def add_to_centre_of_grid(grid, thing):
    """
    thing is a list of relative coordinates
    do add_to_grid, where (x,y) is the centre of the grid
    """
    centre_x = grid.shape[0] / 2
    centre_y = grid.shape[1] / 2
    add_to_grid(grid, thing, centre_x, centre_y)

def toggle_cell(grid, x, y):
    """
    if grid[x, y] is 1, set grid[x, y] to 0
    and vice versa
    """
    if grid[x, y] == 1:
        v = 0
    else:
        v = 1
    grid[x, y] = v


def update(grid, p=None):
    """
    takes a matrix of values (1 or 0) representing the Life game state
    returns the game state, advanced by one step

    p is the probability that a dead cell with 2 neighbours spontaneously becomes alive (zombie?)
    """
    new_grid = np.zeros(grid.shape, dtype=np.uint8)

    # matrix containing the number of neighbours of each cell
    neighbours_grid = np.zeros(grid.shape, dtype=np.uint8)

    # only have to update the live cells and their neighbours
    to_update = set()
    for x, y in np.ndindex(grid.shape):
        if grid[x, y] == 1:
            # reconsider all live cells
            to_update.add( (x, y) )
            for n_x, n_y in get_neighbours(x, y, grid.shape):
                # reconsider all neighbours of live cells
                to_update.add( (n_x, n_y) )

                # can also calculate the number of neighbours in this step
                neighbours_grid[n_x, n_y] += 1

    # actually update the cells
    for x, y in to_update:
        neighbours = neighbours_grid[x, y]
        # apply cell update rule
        if neighbours == 3 or (neighbours == 2 and (grid[x, y] == 1 or probably(p))):
            new_grid[x, y] = 1

    return new_grid


if __name__=="__main__":
    # just a test
    lg = LifeGame(10,10)
    lg.grid[2,5] = 1

    lg.grid[3,6] = 1

    lg.grid[4,4] = 1
    lg.grid[4,5] = 1
    lg.grid[4,6] = 1

    for i in range(10):
        lg.update()
        print lg.grid
        print ""


