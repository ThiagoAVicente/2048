import logging
from game import g2048
from utils.directions import RIGHT, LEFT, UP, DOWN
import os

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s: %(message)s', force=True)


game = g2048()

dictdir ={
    "w":UP,
    "a":LEFT,
    "s":DOWN,
    "d":RIGHT
}

while True:
    #os.system("clear")
    print(game)
    print("w,a,s,d")
    dir = input(">> ")
    op = dictdir[dir]

    if game.play(op) == -2:
        break
