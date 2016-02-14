# -*- coding: utf-8 -*-
from __future__ import division
import argparse
import numpy as np
import pygame

import life

PAUSED_CAPTION = "Game of Life [paused]"
UNPAUSED_CAPTION = "Game of Life"

RED_COLOR = pygame.Color(255, 0, 0)
WHITE_COLOR = pygame.Color(255, 255, 255)


def run(probability=0): 
    # initialize game engine
    pygame.init()

    # set screen width/height and caption
    size = [640, 480]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(UNPAUSED_CAPTION)

    # initially paint the screen white
    screen.fill(WHITE_COLOR)
    pygame.display.update()


    # set the number of cells
    f = 10
    grid_width, grid_height = int(size[0] / f), int(size[1] / f)

    # initialise the game state
    grid = np.zeros((grid_width, grid_height), dtype=np.uint8)
    old_grid = None

    # initialise a 3x1 flippy thing
    life.add_to_centre_of_grid(grid, life.three_bar)

    # dimensions of the rendered cells
    cell_width = size[0] / grid.shape[0]
    cell_height = size[1] / grid.shape[1]

    # Loop until the game quits
    done = False

    # is the game paused?
    paused = False

    # number of iterations made
    i = 0

    # initialize clock
    clock = pygame.time.Clock()

    # game loop
    while not done:
        # event handling stage
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                elif event.key == pygame.K_SPACE:
                    # toggle paused-ness
                    paused = not paused

                    # update the title
                    if paused:
                        pygame.display.set_caption(PAUSED_CAPTION)
                    else:
                        pygame.display.set_caption(UNPAUSED_CAPTION)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # get the clicked cell
                cell_x = mouse_x / cell_width
                cell_y = mouse_y / cell_height

                # toggle the state of the clicked cell
                old_grid[cell_x, cell_y] = grid[cell_x, cell_y]

                life.toggle_cell(grid, cell_x, cell_y)

                # clicking pauses the simulation
                paused = True


        # game logic stage
        if not paused:
            if not grid.any():
                # reset board because it's all dead, jim
                # add that default bit back to it
                life.add_to_centre_of_grid(grid, life.three_bar)

            # advance the game state
            old_grid = grid
            grid = life.update(grid, p=probability)
            i += 1


        # draw/display stage

        # keep track of the modified regions of the screen
        dirty_rects = []

        # iterate over the cells
        for x,y in np.ndindex(grid.shape):
            # avoid redrawing cells that haven't changed
            if old_grid == None or grid[x,y] != old_grid[x,y]:
                # live cells are red, dead cells are white
                if grid[x,y] == 1:
                    c = RED_COLOR
                else:
                    c = WHITE_COLOR

                # draw the cell
                r = pygame.Rect(x*cell_width, y*cell_height, cell_width, cell_height)
                pygame.draw.rect(screen, c, r)

                # mark this part of the screen as modified
                dirty_rects.append(r)

        # display what’s drawn
        pygame.display.update(dirty_rects)

        dt = clock.tick(30)
        #if not paused and i % 50 == 0:
        #    print int(1000 / dt)
    
    # close the window and quit
    pygame.quit()


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Game of Life simulator')
    parser.add_argument('-p', '--probability',
                        help='probability that a cell with two neighbours will spontaneously appear',
                        type=float)
    args = parser.parse_args()
    run(probability=args.probability)
