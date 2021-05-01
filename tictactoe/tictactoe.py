"""
Tic Tac Toe Player
"""

import math
import copy
import random

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


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    y_count = 0

    for row in board:
        x_count += row.count(X)
        y_count += row.count(O)

    return X if x_count == y_count else O
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    all_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                all_actions.add((i, j))
    return all_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result = copy.deepcopy(board)
    i, j = action
    if result[i][j] != EMPTY:
        raise Exception("Invalid action")
    result[i][j] = player(board)
    return result


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        # vertical check
        player = board[0][i]
        if player == board[1][i] == board[2][i]:
            return player
        # horizontal check
        player = board[i][0]
        if player == board[i][1] == board[i][2]:
            return player

    # center
    player = board[1][1]
    if (player == board[0][0] == board[2][2] or
           player == board[0][2] == board[2][0]):
        return player

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or len(actions(board)) == 0:
        return True
    return False


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


def minimax_helper(board):
    if terminal(board):
        return (utility(board), None)

    current_player = player(board)
    all_actions = actions(board)

    if current_player == X:
        best_score = -math.inf
        for action in all_actions:
            new = result(board, action)
            score = minimax_helper(new)[0]
            if score > best_score:
                best_score = score
                best_action = action

        return (best_score, best_action)
    
    if current_player == O:
        best_score = math.inf
        for action in all_actions:
            new = result(board, action)
            score = minimax_helper(new)[0]
            if score < best_score:
                best_score = score
                best_action = action
        return (best_score, best_action)
        

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    return minimax_helper(board)[1]
