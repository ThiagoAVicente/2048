import numpy as np
import logging
from utils.directions import UP, DOWN, LEFT, RIGHT

TARGETVALUE = 2048
logger = logging.getLogger("GAME")

class g2048:
    def __init__(self, size = 4):
        self.size = 4
        self.points = 0
        self.reset()

    def getBoard(self) -> np.ndarray:
        """Get the current game board"""
        return self.board.copy()

    def reset(self) -> int:
        """
        resets game
        :returns points on previous game
        """
        points = self.points

        #reset game status
        self.board  = np.zeros((self.size,self.size))
        self.__spawn()
        self.points = 0
        self.done = False
        logger.info(f"Game with {points} reseted")
        return points

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

        return -go if go < 4 and go > 1 else points

    def __exec(self,direction) -> int:

        vertical = direction[0]

        if abs(vertical):
            return self.__vertical_move(vertical)

        return self.__horizontal_move(direction[1])


    def __vertical_move(self, dir:int)->int:
        points = 0
        limits = [-1 for i in range(0,self.size)]
        moved = False

        # iterate in inverse order
        start = 0 if dir == -1 else self.size-1
        my = -dir

        for column in range(self.size):

            counter = start
            while counter >= 0 and counter < self.size:
                current = counter
                counter += my

                value = self.board[current,column]

                # skip empty rows
                if value == 0 :
                    continue

                if limits[column] == current:
                    continue

                if limits[column] < 0:
                    # move to limit
                    new_limit = 0 if dir == -1 else self.size-1
                    limits[column] = new_limit
                    moved |= self.__move(current,column, new_limit,column)
                    continue

                target_value = self.board[limits[column],column]
                if target_value == value:
                    # merge tiles and add points
                    moved |= self.__move(current,column,limits[column],column)
                    self.board[limits[column],column] *= 2
                    points += self.board[limits[column],column]
                    continue

                # place tile next to the other
                new_limit = limits[column] + my
                moved |= self.__move(current,column, new_limit,column)
                limits[column] = new_limit

        return points if moved else -1

    def __move(self,x,y,nx,ny):

        if x == nx and y == ny:
            return False

        value = self.board[x,y]
        self.board[x,y] = 0
        self.board[nx,ny] = value
        return True

    def __horizontal_move(self, dir:int)->int:
        points = 0
        limits = [-1 for i in range(0,self.size)]
        moved = False
        # iterate in inverse order
        start = 0 if dir == -1 else self.size-1
        mx = -dir

        for row in range(self.size):

            counter = start
            while counter >= 0 and counter < self.size:
                current = counter
                counter += mx

                value = self.board[row,current]

                # skip empty rows
                if value == 0 :
                    continue

                if limits[row] == current:
                    continue

                if limits[row] < 0:
                    # move to limit
                    new_limit = 0 if dir == -1 else self.size-1
                    limits[row] = new_limit
                    moved |=  self.__move(row,current,row,new_limit)
                    continue

                target_value = self.board[row,limits[row]]
                if target_value == value:
                    # merge tiles and add points
                    moved |= self.__move(row,current,row,limits[row])
                    self.board[row,limits[row]] *= 2
                    points += self.board[row,limits[row]]
                    continue

                # place tile next to the other
                new_limit = limits[row] + mx
                moved |= self.__move(row,current,row,new_limit)
                limits[row] = new_limit

        return points if moved else -1

    def __is_game_over(self) -> int:
        """
        :returns
            1 - game is not over
            2 - player lost
            3 - player won
        """

        dirs = [UP,DOWN,LEFT,RIGHT]

        for index, value in np.ndenumerate(self.board):

            # board is not full
            if value == 0:
                return 1

            if value == TARGETVALUE:
                return 3

            # check possibilities in every direction
            for dir in dirs:
                x,y  = index[0] + dir[0], index[1] + dir[1]
                if x < self.size and x >= 0 and y < self.size and y >= 0:
                    tvalue = self.board[x,y]

                    if tvalue == value or tvalue == 0:
                        return 1

                    if tvalue == TARGETVALUE:
                        return 3

        return 2


    def __spawn(self) -> bool:
        """
        spawn a random piece in the board
        :returns False if board is full
        """
        value = np.random.choice([2, 4], p=[0.9, 0.1])
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
