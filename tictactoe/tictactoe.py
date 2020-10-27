"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
score= [0] * 100
EMPTY = None

import sys
sys.setrecursionlimit(1500)

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

# Checks which players turn it is
def player(board):
    x_count = 0
    o_count = 0
    # As X always starts I can count numner of x's and o's and alternate player once one is added
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == X:
                x_count += 1
            if board[y][x] == O:
                o_count += 1
    if x_count > o_count:
        return O
    else:
        return X
# Function that checks number of turns that have been played, using same logic as previous function
def depth(board):
    x_num = 0
    o_num = 0
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == X:
                x_num += 1
            if board[y][x] == O:
                o_num += 1

    count = x_num + o_num
    return count
# Finds all possible moves a player can make
def actions(board):
    poss_moves = list()
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == EMPTY:
                temp = [0] * 2
                temp[0] = x
                temp[1] = y
                # Loops through entire list and checks for an empty index. If found, it appends the location to a list
                poss_moves.append(temp)
    return poss_moves
    


# Returns a deepcopy of the board with the included action now being filled with the player's symbol
def result(board, action):
    newBoard = copy.deepcopy(board)
    # If space isn't free, program exits
    if board[action[0]][action[1]] != EMPTY:
        raise Exception
    else:
        newBoard[action[0]][action[1]] = player(board)
    return newBoard

# Checks whole board for a diagonal, horizontal or vertical win condition
def winner(board):
    countHo = [0] * 3
    countHx = [0] * 3
    countVo = [0] * 3
    countVx = [0] * 3
    RightDiagPos = [0] * 3
    LeftDiagPos = [0] * 3
    countDxR = [0] * 3
    countDoR = [0] * 3
    countDoL = [0] * 3
    countDxL = [0] * 3
    # Loops through whole board looking for indicators that a condition can't be true
    # i.e If there is an O in a column, that column can't be an X win
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[x][y] == O or board[x][y] == EMPTY:
                countVx[y] += 1
            if board[x][y] == X or board[x][y] == EMPTY:
                countVo[y] += 1
            if board[y][x] == O or board[y][x] == EMPTY:
                countHx[y] += 1
            if board[y][x] == X or board[y][x] == EMPTY:
                countHo[y] += 1
            # Diagonal characters are collected and checked seperately
            if x == y:
                RightDiagPos[x] = (board[y][x])
            if y == x - 2 or x == y - 2 or y == 1 and x == 1:
                LeftDiagPos[x] = (board[y][x])
    # Same procedure for horizontals and verticals, but now for diagonals wins
    for y in range(len(board)):
        for x in range(len(board[y])):
            if RightDiagPos[x] == O or RightDiagPos[x] == EMPTY:
                countDxR[y] += 1
            if LeftDiagPos[x] == O or LeftDiagPos[x] == EMPTY:
                countDxL[y] += 1
            if RightDiagPos[x] == X or RightDiagPos[x] == EMPTY:
                countDoR[y] += 1
            if LeftDiagPos[x] == X or LeftDiagPos[x] == EMPTY:
                countDoL[y] += 1

    # Finally the function concludes that if there is no presence of condradictory proofs, then the player must have won
    if 0 in countHo  or 0 in countVo  or 0 in countDoR or 0 in countDoL:
        return O
    if 0 in countHx or 0 in countVx or 0 in countDxR or 0 in countDxL:
        return X
    else:
        return None

# Checks if game has concluded
def terminal(board):
    # Checks conditions that would mean an ending
    if depth(board) == 9 or winner(board) == X or winner(board) == O:
        return True
    # If not found, game can't have finished
    else:
        return False


# If program has finished, a score is given to any winner
def utility(board):
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    if winner(board) == None and terminal(board) ==  True:
        return 0
    elif terminal(board) == False:
        return None

# Decides which move is optimal according to another function
def minimax(board):
    # Decides whether or not to min or max score
    if player(board) == X:
        TopScore = -2
    if player(board) == O:
        TopScore = 2
    # If player is X and move is the initial, then best move will always be the same as X starts
    # Without this, the program would run very slowly as time to run increases exponentially due to the recursive algorithm
    BestAction = [0] * 2
    if depth(board) == 0 and player(board) == X:
        BestAction[0] == 0
        BestAction[1] == 0
        return BestAction
    moves = actions(board)
    for x in range(len(moves)):
        board[moves[x][1]][moves[x][0]] = player(board)
        score = BestScore(board)
        board[moves[x][1]][moves[x][0]] = EMPTY
        # If calculated score of AI is greatest so far, then the corresponding move is now the best
        # For X player who is maximising
        if score > TopScore and player(board) == X:
            TopScore = score
            BestAction[0] = moves[x][1]
            BestAction[1] = moves[x][0]
        # Same thing as above but for minimising player
        elif score < TopScore and player(board) == O:
            TopScore = score
            BestAction[0] = moves[x][1]
            BestAction[1] = moves[x][0]

    return BestAction



# The actual minmax algorithm with evaluates a score of the move recursively
def BestScore(board):
    # If game is in a terminal state, the score of that board is returned
    if terminal(board) == True:
        return utility(board)
    # Player X wishes to maximise the score
    if player(board) == X:
        TopScore = float("-inf")
        # Gets all possible moves
        moves = actions(board)
        for u in range(len(moves)):
            # Calculates a score for each move by calling itself until terminal state
            board[moves[u][1]][moves[u][0]] = X
            score = BestScore(board)
            # Reset the board
            board[moves[u][1]][moves[u][0]] = EMPTY
            # Checks to see wether or not this move is maximizing the score
            if score > TopScore:
                TopScore = score


        return TopScore
    # Player O wishes to minimise the score
    if player(board) == O:
        TopScore = float("inf")
        moves = actions(board)
        for u in range(len(moves)):
            board[moves[u][1]][moves[u][0]] = O
            score = BestScore(board)
            board[moves[u][1]][moves[u][0]] = EMPTY
            # Checks whether or not this move is the minimising move
            if score < TopScore:
                TopScore = score

        return TopScore
























