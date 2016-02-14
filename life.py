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


class LifeGame(object):
    def __init__(self, width, height):
        self.grid = np.zeros((width, height), dtype=np.uint8)
        self.old_grid = None

    def add_to_grid(self, thing, x, y):
        for c_x, c_y in thing:
            self.grid[x+c_x, y+c_y] = 1

    def add_to_centre_of_grid(self, thing):
        centre_x = self.grid.shape[0] / 2
        centre_y = self.grid.shape[1] / 2
        self.add_to_grid(thing, centre_x, centre_y)

    def toggle_cell(self, x, y):
        if self.grid[x, y] == 1:
            v = 0
        else:
            v = 1
        self.old_grid[x, y] = self.grid[x, y]
        self.grid[x, y] = v

    def update(self, p=None):
        new_grid = np.zeros(self.grid.shape, dtype=np.uint8)

        # matrix containing the number of neighbours of each cell
        neighbours_grid = np.zeros(self.grid.shape, dtype=np.uint8)

        # only have to update the live cells and their neighbours
        to_update = set()
        for x, y in np.ndindex(self.grid.shape):
            if self.grid[x, y] == 1:
                # reconsider all live cells
                to_update.add( (x, y) )
                for n_x, n_y in get_neighbours(x, y, self.grid.shape):
                    # reconsider all neighbours of live cells
                    to_update.add( (n_x, n_y) )

                    # can also calculate the number of neighbours in this step
                    neighbours_grid[n_x, n_y] += 1

        # actually update the cells
        for x, y in to_update:
            neighbours = neighbours_grid[x, y]
            # apply cell update rule
            if neighbours == 3 or (neighbours == 2 and (self.grid[x, y] == 1 or probably(p))):
                new_grid[x, y] = 1

        # old_grid is used in the draw cycle
        self.old_grid = self.grid
        self.grid = new_grid



if __name__=="__main__":
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


