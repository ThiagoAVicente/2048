import numpy as np
import logging
from utils.directions import UP, DOWN, LEFT, RIGHT
from utils.boardmoves import horizontal_move, vertical_move
from utils.rules import TILE_PROBABILITY

TARGETVALUE = 2048
logger = logging.getLogger("GAME")

class g2048:
    def __init__(self, size = 4):
        self.size = 4
        self.reset()
    def getPoints(self):
        return np.max(self.board)
    def getBoard(self) -> np.ndarray:
        """Get the current game board"""
        return self.board.copy()

    def reset(self):
        """
        resets game
        :returns points on previous game
        """
        #reset game status
        self.board  = np.zeros((self.size,self.size))
        self.__spawn()
        self.done = False

    def play(self, direction) -> int:
        """
        Make a play
        :direction: utils.directions -> direction to move pieces
        :returns the amount of points that were made by the movement, note that returning -1 means that no movement was made and -2 means game is over and player lost, -3 means player won
        """

        # game already over
        if self.done:
            return -2

        points:int = self.__exec(direction)
        if points < 0:
            # Cannot move pieces in that direction
            return -1
        self.__spawn()
        go = abs(self.__is_game_over())
        return -go if go > 1 else points

    def __exec(self,direction) -> int:

        vertical = direction[0]

        if abs(vertical):
            return vertical_move(vertical,self.board,self.size)

        return horizontal_move(direction[1],self.board,self.size)

    def __is_game_over(self) -> int:
        """
        :returns
            1 - game is not over
            2 - player lost
            3 - player won
        """

        dirs = [UP,DOWN,LEFT,RIGHT]
        visited = np.zeros((self.size,self.size))
        visited = np.array(visited,dtype = bool)

        for index, value in np.ndenumerate(self.board):
            visited[index] = True # mark path

            # case 1: empty tile
            if np.isclose(value,0):
                return 1

            for direction in dirs:
                nx, ny = index[0] + direction[0], index[1] + direction[1]

                # check limits
                if nx < 0 or nx >= self.size or ny < 0 or ny >= self.size:
                    continue

                # no need to check again
                if visited[nx,ny]:
                    continue

                tvalue = self.board[nx,ny]

                # case 1: possible merge
                if np.isclose(tvalue,value):
                    return 1

                if np.isclose(tvalue,TARGETVALUE) or np.isclose(value,TARGETVALUE):
                    return 3

        return 2

    def __spawn(self) -> bool:
        """
        spawn a random piece in the board
        :returns False if board is full
        """
        value = np.random.choice(TILE_PROBABILITY["values"], p=TILE_PROBABILITY["prob"])
        empty_tiles = np.argwhere(self.board == 0)
        # board is full
        if len(empty_tiles) == 0:
            return False

        # choose a position to create tile
        icoord = np.random.choice(list(range(0, len(empty_tiles))))
        coord = empty_tiles[icoord]
        self.board[coord[0],coord[1]] = value

        return True

    def __str__(self):
        return str(self.board)
