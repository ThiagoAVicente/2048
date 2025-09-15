import logging
from game.autoPlay import playGame
from game.game import g2048
from utils.directions import RIGHT, LEFT, UP, DOWN
import agents.expectiminimax as emm
import os
from utils.displayer import display_board
import time

AGENT_DEPTH:int = 1

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s: %(message)s', force=True)
logger = logging.getLogger("Main")
game = g2048()
agent = emm.agent(AGENT_DEPTH)

dictdir ={
    "w":UP,
    "a":LEFT,
    "s":DOWN,
    "d":RIGHT
}

def displayCaller(game,op):
    board = game.getBoard()
    display_board(board,op)

points = playGame(agent,displayCaller)
print(f"Ended game with {points} points")
