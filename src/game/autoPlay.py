from game.game import  g2048
import os

def playGame(moves)-> int:
    """
    Auto play 2048 using moves
    :moves -> param that contains a data structure/object that contains a method .act(np.ndArray) and returns a tuple with 2 elements representing the direction
    """
    game = g2048()
    while True:
        op = moves.act(game.getBoard())
        res = game.play(op)
        if  res < 0:
            break
    return int(game.getPoints())
