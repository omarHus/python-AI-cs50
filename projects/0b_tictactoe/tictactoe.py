"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def test_state():
    return [[X, EMPTY, O],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY,EMPTY, X]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    currentPlayer = X
    # X is always the first person to play, so if there are an even# of empty tiles then it is O's turn
    emptyCount = sum(row.count(EMPTY) for row in board)
    if (emptyCount % 2 == 0):
        currentPlayer = O
    
    return currentPlayer
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []

    for i in range(len(board)):
        for j in range(len(board)):
            # if the cell is empty it is a legal move
            row = board[i]
            col = row[j]
            if col == EMPTY:
                action = (i, j)
                actions.append(action)          
    return actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # check if action is valid
    try:
        if board[action[0]][action[1]] != EMPTY:
            raise IndexError
        else:
            # figure out whose turn it is
            currentPlayer = player(board)
            # make a deepcopy of the board
            newBoard = deepcopy(board)
            # update newBoard to reflect action taken, 
            newBoard[action[0]][action[1]] = currentPlayer
            return newBoard
    except IndexError:
        print("Spot already occupied")

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    diagIndex = 0
    diagIndex2 = 2
    diag1 = []
    diag2 = []
    for i in range(len(board)):
        # Check for winning rows
        winner = whoWon(board[i])
        row = board[i]
        if winner != EMPTY:
            return winner

        col = []
        for j in range(len(board[i])):
            col.append(board[j][i])  
        # Check for winning column
        winner = whoWon(col)
        if winner != EMPTY:
            return winner
        # make diagonals
        diag1.append(board[i][diagIndex])
        diag2.append(board[i][diagIndex2])
        diagIndex += 1
        diagIndex2 -= 1
    #check diagonals
    winner = whoWon(diag1)
    if winner == EMPTY:
        winner = whoWon(diag2)
    return winner


def whoWon(row):
    if row.count(X) == 3:
        return X
    elif row.count(O) == 3:
        return O
    else:
        return EMPTY
       

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # game can be over if someone won or there are no more empties
    return (winner(board) != EMPTY or sum(row.count(EMPTY) for row in board) < 1)



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

# def minimax(board):
#     """
#     Returns the optimal action for the current player on the board.
#     """
#     if terminal(board):
#         return None

#     # get the player's turn
#     currentPlayer = player(board)
#     depth = 4
#     alpha = -1000
#     beta = 1000
#     if currentPlayer == X:
#         k = -1000

#         for action in actions(board):
#             k = max(k, min_value(result(board, action), -1000, 1000, depth))
#             alpha = max(k, alpha)
#             bestAction = action
#             if alpha >= beta:
#                 bestAction = action
#                 return bestAction
#     else:
#         k = 1000
#         for action in actions(board):
#             k = min(k, max_value(result(board, action), -1000, 1000, depth))
#             beta = min(k, beta)
#             bestAction = action
#             if alpha >= beta:
#                 bestAction = action
#                 return bestAction
#     return bestAction


# def max_value(board, alpha, beta, depth):

#     if terminal(board):
#         return utility(board)
    
#     # recursive call to see how the game unfolds for given actions
#     v = -1000
#     for action in actions(board):
#         # depth -=1
#         v = max(v, min_value(result(board, action), alpha, beta, depth))
#         # print(f"vmax is {v}, alpha is {alpha}, beta is {beta} and action is {action}")
#         alpha = max(v, alpha)
#         if alpha >= beta:
#             break
#     return v

# def min_value(board, alpha, beta, depth):
#     if terminal(board):
#         return utility(board)
    
#     v = 1000
#     for action in actions(board):
#         # depth -= 1
#         v = min(v, max_value(result(board, action), alpha, beta, depth))
#         # print(f"vmin is {v}, alpha is {alpha}, beta is {beta} and action is {action}")
#         beta = min(beta, v)
#         if alpha >= beta:
#             break
#     return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    currentactions = actions(board)
    if player(board) == X:
        vT = -math.inf
        move = set()
        for action in currentactions:
            v, count = minvalue(result(board,action), -math.inf, math.inf, 0)
            if v > vT:
                vT = v
                move = action
    else:
        vT = math.inf
        move = set()
        for action in currentactions:
            v, count = maxvalue(result(board,action), -math.inf, math.inf, 0)
            if v < vT:
                vT = v
                move = action
    print(count)
    return move

def maxvalue(board,alpha,beta,count):
    """
    Calculates the max value of a given board recursively together with minvalue
    """

    if terminal(board): return utility(board), count+1

    v = -math.inf
    posactions = actions(board)

    for action in posactions:
        vret, count = minvalue(result(board, action),alpha,beta,count)
        v = max(v, vret)
        alpha = max(alpha, v)
        if alpha > beta:
            break
    return v, count+1

def minvalue(board,alpha,beta,count):
    """
    Calculates the min value of a given board recursively together with maxvalue
    """

    if terminal(board): return utility(board), count+1

    v = math.inf
    posactions = actions(board)

    for action in posactions:
        vret, count = maxvalue(result(board, action),alpha,beta,count)
        v = min(v, vret)
        beta = min(v, beta)
        if alpha > beta:
            break
    return v, count + 1