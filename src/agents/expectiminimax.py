"""
expectiminimax is a adversarial searching algorithm similar to minimax
but it is non deterministic. So it works with probabilities
https://en.wikipedia.org/wiki/Expectiminimax
"""

from typing import Optional
from numpy._core.numeric import inf
import logging

from utils.rules import TILE_PROBABILITY
from utils.boardmoves import horizontal_move, vertical_move, is_full, get_empty, get_legal_moves
import numpy as np
from utils.directions import UP

logger = logging.getLogger("Emm")

class agent:
    def __init__(self,maxdepth:int = 3,size = 4, w_empty = 0.5, w_max = 0.5):
        self.maxdepth = maxdepth
        self.size = size
        self.w_empty = w_empty
        self.w_max = w_max
        logger.info(f"Emm agent with {maxdepth} maxdepth")

    def act(self, board:np.ndarray, *args ):
        score = -inf
        best_move = UP
        for move in get_legal_moves(board,self.size):
            new_board = self.__move(board,move,self.size)
            new_score = self.__expectiminimax(new_board,self.size,self.maxdepth)
            if  new_score > score:
                best_move = move
                score = new_score
            
        return best_move

    def __expectiminimax(self,board,size, depth, isMaxNode=True) -> float:
        """
        find best play
        This is not the original algorithm because in 2048 there is no adversary playing against the agent. We will consider tile spawn in this calculus and also will use the original game probabilities: 2-90% and 4-10%
        """

        if is_full(board) or depth == 0:
            return self.__valueOf(board)

        if isMaxNode:
            # find movement with best score
            best_score = -inf
            for move in get_legal_moves(board,size):

                new_board = self.__move(board,move,size)
                if new_board is None:
                    #illegal move
                    continue
                best_score = max(best_score,self.__expectiminimax(new_board,size,depth-1,False))
            return best_score

        # in this part it's different from minimax
        # We will some all the child probabilities in order to build the expected value
        childs = get_empty(board)
        prob = 1/len(childs)
        expected_value = 0

        for child in childs:
            for value,probability in zip(TILE_PROBABILITY["values"],TILE_PROBABILITY["prob"]):
                child_board = self.__place_tile(board,value,child[0],child[1])
                maxResult = self.__expectiminimax(child_board,size,depth-1,True)
                expected_value += prob * probability * maxResult
        return expected_value


    def __place_tile(self,board,value,x,y):
        new_board = board.copy()
        new_board[x,y] = value
        return new_board

    def __move(self, board, direction, size)-> Optional[np.ndarray]:
        """
        returns the updated table
        CREATES A NEW ARRAY
        """
        new_board = board.copy()
        vertical = direction[0]

        if abs(vertical):
            moved = vertical_move(vertical,new_board,self.size)
        else:
            moved = horizontal_move(direction[1],new_board,self.size)

        return new_board if moved != -1 else None

    def __valueOf(self, board) -> float:
        empty_cells = len(get_empty(board))
        max_tile = np.max(board)

        return self.w_empty * empty_cells + self.w_max * max_tile
