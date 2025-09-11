from typing import List
import numpy as np

from utils.directions import UP, DOWN, RIGHT, LEFT

def __move(x,y,nx,ny,board):

    if x == nx and y == ny:
        return False

    value = board[x,y]
    board[x,y] = 0
    board[nx,ny] = value
    return True


def get_legal_moves(board,size) -> List:
    possibles = [UP,DOWN,RIGHT,LEFT]
    res = []
    test_board = board.copy()
    for direction in possibles:
        vertical = direction[0]

        if abs(vertical):
            legal = vertical_move(vertical,test_board,size) != -1
        else:
            legal = horizontal_move(direction[1],test_board,size) != -1

        if legal:
            res.append(direction)
            test_board = board.copy() # restore initial state

    return res

def vertical_move( dir:int, board,size)->int:
    points = 0
    limits = [-1 for i in range(0,size)]
    moved = False

    # iterate in inverse order
    start = 0 if dir == -1 else size-1
    my = -dir

    for column in range(size):

        counter = start
        while counter >= 0 and counter < size:

            current = counter
            counter += my

            value = board[current,column]

            # skip empty rows
            if value == 0 :
                continue

            if limits[column] == current:
                continue

            if limits[column] < 0:
                # move to limit
                new_limit = 0 if dir == -1 else size-1
                limits[column] = new_limit
                moved |= __move(current,column, new_limit,column,board)
                continue

            target_value = board[limits[column],column]
            if target_value == value:
                # merge tiles and add points
                moved |= __move(current,column,limits[column],column,board)
                board[limits[column],column] *= 2
                points += board[limits[column],column]
                continue

            # place tile next to the other
            new_limit = limits[column] + my
            moved |= __move(current,column, new_limit,column,board)
            limits[column] = new_limit

    return points if moved else -1

def is_full(board):
    # board is full
    if len(get_empty(board)) == 0:
        return False

def get_empty(board):
    return np.argwhere(board == 0)

def horizontal_move(dir:int,board,size)->int:
    points = 0
    limits = [-1 for i in range(0,size)]
    moved = False
    # iterate in inverse order
    start = 0 if dir == -1 else size-1
    mx = -dir

    for row in range(size):

        counter = start
        while counter >= 0 and counter < size:
            current = counter
            counter += mx

            value = board[row,current]

            # skip empty rows
            if value == 0 :
                continue

            if limits[row] == current:
                continue

            if limits[row] < 0:
                # move to limit
                new_limit = 0 if dir == -1 else size-1
                limits[row] = new_limit
                moved |=  __move(row,current,row,new_limit,board)
                continue

            target_value = board[row,limits[row]]
            if target_value == value:
                # merge tiles and add points
                moved |= __move(row,current,row,limits[row],board)
                board[row,limits[row]] *= 2
                points += board[row,limits[row]]
                continue

            # place tile next to the other
            new_limit = limits[row] + mx
            moved |= __move(row,current,row,new_limit,board)
            limits[row] = new_limit

    return points if moved else -1
