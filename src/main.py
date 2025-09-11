import logging
from game.game import g2048
from utils.directions import RIGHT, LEFT, UP, DOWN
import agents.expectedminimax as emm
import os

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
    os.system("clear")
    print(game)

    op = agent.act(game.getBoard())
    res = game.play(op)
    if  res <= -2:
        break

os.system("clear")
print(game)
