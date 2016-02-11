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
        return True

def get_neighbours(x, y, width, height):
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
        self.width = width
        self.height = height
        self.grid = np.zeros((self.width, self.height), dtype=np.uint8)
        self.old_grid = None

    def add_to_grid(self, thing, x, y):
        for c_x, c_y in thing:
            self.grid[x+c_x, y+c_y] = 1

    def add_to_centre_of_grid(self, thing):
        centre_x = self.width / 2
        centre_y = self.height / 2
        self.add_to_grid(thing, centre_x, centre_y)

    def count_neighbours(self, x, y):
        s = 0

        if x > 0:
            if y > 0:
                s += self.grid[x-1, y-1]
            if y < self.height - 1:
                s += self.grid[x-1, y+1]
            s += self.grid[x-1, y]

        if x < self.width - 1:
            if y > 0:
                s += self.grid[x+1, y-1]
            if y < self.height - 1:
                s += self.grid[x+1, y+1]
            s += self.grid[x+1, y]

        if y > 0:
            s += self.grid[x, y-1]
        if y < self.height - 1:
            s += self.grid[x, y+1]

        return s

    def toggle_cell(self, x, y):
        if self.grid[cell_x, cell_y] == 1:
            self.grid[cell_x, cell_y] = 0
        else:
            self.grid[cell_x, cell_y] = 1


    def update(self, p=None):
        new_grid = np.zeros((self.width, self.height), dtype=np.uint8)

        # only have to update the live cells and their neighbours
        to_update = set()
        for i in range(self.width):
            for j in range(self.height):
                if self.grid[i,j] == 1:
                    to_update.add( (i,j) )
                    for nbr in get_neighbours(i, j, self.width, self.height):
                        to_update.add(nbr)

        for i,j in to_update:
            neighbours = self.count_neighbours(i,j)
            if neighbours == 3 or (neighbours == 2 and (self.grid[i,j] == 1 or probably(p))):
                new_grid[i,j] = 1

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


