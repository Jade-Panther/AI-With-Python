"""
Tic Tac Toe Player
"""

import math

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
    emptyCount = 0
    for row in board:
        emptyCount += row.count(EMPTY)

    return X if emptyCount % 2 == 1 else O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    allActions = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                allActions.add((i, j))
    return allActions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception('InvalidActionError')
    
    copyBoard = []
    for row in board:
        copyBoard.append([])
        for colm in row:
            copyBoard[-1].append(colm)
    
    symbol = player(copyBoard)
    copyBoard[action[0]][action[1]] = symbol

    return copyBoard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    for i in range(3):
        # Check rows
        row = board[i]
        if row[0] == row[1] == row[2] != EMPTY:
            return row[0]
        
        # Check columns
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
            
    #Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    
    return None
        
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    
    for row in board:
        for colm in row:
            if colm == EMPTY:
                return False
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    return 0

def maxAction(board):
    if terminal(board):
        return (utility(board), None)
    
    v = -math.inf
    maxAction = (0, 0)
    for action in actions(board):
        val = minAction(result(board, action))
        
        val = val[0]
        if val > v:
            v = val
            maxAction = action
       
    return (v, maxAction)

def minAction(board):
    if terminal(board):
        return (utility(board), None)
    
    v = math.inf
    minAction = (0, 0)
    for action in actions(board):
        val = maxAction(result(board, action))[0]
        if val < v:
            v = val
            minAction = action
    return (v, minAction)

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    if player(board) == X:
        return maxAction(board)[1]
    else:
        return minAction(board)[1]
