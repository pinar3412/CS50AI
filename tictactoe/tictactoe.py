"""
Tic Tac Toe Player
"""
import copy
import math
import numpy as np


X = "X"
O = "O"
EMPTY = None
set1 = range(0, 3)


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    countx = 0
    counto = 0

    for i in set1:
        for j in set1:
            if board[i][j] == X:
                countx += 1
            elif board[i][j] == O:
                counto += 1

    if countx <= counto:
        return X
    else:
        return O


def actions(board):
    set2 = []
    for i in set1:
        for j in set1:
            if board[i][j] == EMPTY:
                set2.append((i, j))
                print("action",i,j)

    return set2


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board2 = copy.deepcopy(board)

   # print("a", action)

    # i,j =action
    # print(i)
    # print(j)

    if board2[action[0]][action[-1]] == EMPTY:
        a = player(board2)
        board2[action[0]][action[-1]] = a
        return board2

    else:
        raise Exception


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    diagx = 0
    diago = 0
    for i in set1:
        if board[i][i] == X:
            diagx += 1
        elif board[i][i] == O:
            diago += 1
    # print(diagx)
    if diagx == 3:
        return X
    elif diago == 3:
        return O

    diagonalx = 0
    diagonalo = 0
    for i in set1:
        if board[i][2 - i] == X:
            diagonalx += 1
        elif board[i][2 - i] == O:
            diagonalo += 1
    if diagonalx == 3:
        return X
    elif diagonalo == 3:
        return O

    for i in set1:
        countx = 0
        counto = 0
        for j in set1:
            if board[i][j] == X:
                countx += 1
            elif board[i][j] == O:
                counto += 1
        if countx == 3:
            return X
        elif counto == 3:
            return O

    for j in set1:
        countx = 0
        counto = 0
        for i in set1:
            if board[i][j] == X:
                countx += 1
            elif board[i][j] == O:
                counto += 1
        if countx == 3:
            return X
        elif counto == 3:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True

    for i in set1:
        for j in set1:
            if board[i][j] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    #if terminal(board):

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    def Max_value(board):

        if terminal(board):
            return utility(board)

        v = -99999999

        for i, j in actions(board):
            action = (i, j)
            v = max(v, Min_value(result(board, action)))

        return v

    def Min_value(board):

        if terminal(board):
            return utility(board)

        v = 99999999

        for i, j in actions(board):
            action = (i, j)
            v = min(v, Max_value(result(board, action)))
        return v

    if player(board) == X:
        print(board)
        z =-9999999
        for i, j in actions(board):
            #print(i,j)
            action = (i, j)
            z = max(z,Min_value(result(board, action)))


            if z == Max_value(board):
                return action

    else:
        z = 9999999
        for i, j in actions(board):
            action = (i, j)
            z = min(z, Max_value(result(board, action)))

            if z == Min_value(board):
                return action


pinar = initial_state()
# print(player(pinar))
# (actions(pinar))
# print(result(pinar, (0, 0)))
# print(winner(pinar))
# print(terminal(pinar))
# print(utility(pinar))
#print(minimax(pinar))
