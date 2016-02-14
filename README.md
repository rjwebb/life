# 'life'

a game of life simulator, written in python with pygame and numpy

it can be run with ````python main.py```` and you can use the ````-h```` flag to see command line options.

press space to pause, click on a cell to toggle its alive/dead state.

it provides a fun and pretty wild element of randomness, which i will call the __zombie rule__.

## the zombie rule
> every step, each dead cell with two neighbours can spontaneously come alive, as if animated by some dark magic force

use the -p [number] option to set the probability.

if you set it to something low-ish like 0.02 then you will get a nice balance between serentipitous fun chaotic patterns and recognisable Game of Life tropes™ such as the Glider, the Beehive and the Blinker.
