import logging
from game.game import g2048
from utils.directions import RIGHT, LEFT, UP, DOWN
import agents.expectiminimax as emm
import os
from utils.displayer import display_board
import time

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s: %(message)s', force=True)
logger = logging.getLogger("Main")
game = g2048()
agent = emm.agent(3)

dictdir ={
    "w":UP,
    "a":LEFT,
    "s":DOWN,
    "d":RIGHT
}

while True:
    op = agent.act(game.getBoard())
    res = game.play(op)

    # display
    board_np = game.getBoard()
    display_board(board_np,op)
    time.sleep(0.2)

    if  res <= -2:
        break
