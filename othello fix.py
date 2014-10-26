# Othello case study
# This is a slightly-modified version of code written in class
# on Thu 21-Feb-13.  And so it is not commented, and may have
# a bug lurking here or there...

def make2dList(rows, cols):
    a=[]
    for row in xrange(rows): a += [[0]*cols]
    return a

def hasMove(board, player):
    (rows, cols) = (len(board), len(board[0]))
    for row in xrange(rows):
        for col in xrange(cols):
            if (hasMoveFromCell(board, player, row, col)):
                return True
    return False

def hasMoveFromCell(board, player, startRow, startCol):
    (rows, cols) = (len(board), len(board[0]))
    if (board[startRow][startCol] != 0):
        return False
    for dir in xrange(8):
        if (hasMoveFromCellInDirection(board, player, startRow, startCol, dir)):
            return True
    return False

def hasMoveFromCellInDirection(board, player, startRow, startCol, dir):
    (rows, cols) = (len(board), len(board[0]))
    dirs = [ (-1, -1), (-1, 0), (-1, +1),
             ( 0, -1),          ( 0, +1),
             (+1, -1), (+1, 0), (+1, +1) ]
    (drow,dcol) = dirs[dir]
    i = 1
    while True:
        row = startRow + i*drow
        col = startCol + i*dcol
        if (row < 0):
            row += rows
        if (col < 0):
            col += cols
        if (row >= rows):
            row -= rows
        if (col >= cols):
            col -= cols
            
        if (board[row][col] == 0):
            # no blanks allowed in a sandwich!
            return False
        elif (board[row][col] == player):
            # we found the other side of the 'sandwich'
            break
        else:
            # we found more 'meat' in the sandwich
            i += 1
    return (i > 1)

def makeMove(board, player, startRow, startCol):
    # assumes the player has a legal move from this cell
    (rows, cols) = (len(board), len(board[0]))
    for dir in xrange(8):
        if (hasMoveFromCellInDirection(board, player, startRow, startCol, dir)):
            makeMoveInDirection(board, player, startRow, startCol, dir)
    board[startRow][startCol] = player

def makeMoveInDirection(board, player, startRow, startCol, dir):
    (rows, cols) = (len(board), len(board[0]))
    dirs = [ (-1, -1), (-1, 0), (-1, +1),
             ( 0, -1),          ( 0, +1),
             (+1, -1), (+1, 0), (+1, +1) ]
    (drow,dcol) = dirs[dir]
    i = 1
    while True:
        row = startRow + i*drow
        col = startCol + i*dcol

        if (row < 0):
            row += rows
        if (col < 0):
            col += cols
        if (row >= rows):
            row -= rows
        if (col >= cols):
            col -= cols
            
        if (board[row][col] == player):
            # we found the other side of the 'sandwich'
            break
        else:
            # we found more 'meat' in the sandwich, so flip it!
            board[row][col] = player
            i += 1

def getPlayerLabel(player):
    labels = ["-", "X", "O"]
    return labels[player]

def printColLabels(board):
    (rows, cols) = (len(board), len(board[0]))
    print "  ", # skip row label
    for col in xrange(cols): print chr(ord("A")+col),
    print

def printBoard(board,currentPlayer):
    (rows, cols) = (len(board), len(board[0]))
    printColLabels(board)
    for row in xrange(rows):
        print "%2d" % (row+1),
        for col in xrange(cols):
            if ((row,col) in getLegalMoves(board,currentPlayer)):
                print ".",
            else:
                print getPlayerLabel(board[row][col]),
        print "%2d" % (row+1)
    printColLabels(board)

def isLegalMove(board, player, row, col):
    (rows, cols) = (len(board), len(board[0]))
    if ((row < 0) or (row >= rows) or (col < 0) or (col >= cols)): return False
    return hasMoveFromCell(board, player, row, col)

def getMove(board, player):
    print "\n**************************"
    printBoard(board,player)
    while True:
        prompt = "Enter move for player " + getPlayerLabel(player) + ": "
        move = raw_input(prompt).upper()
        # move is something like "A3"
        if ((len(move) < 2) or (len(move) > 3) or (not move[0].isalpha()) or (
            not move[1].isdigit())):
            print "Wrong format!  Enter something like A3 or D5."
        elif (len(move) == 3) and ((not move[2].isdigit()) or (move[1] == 0)):
            print "Wrong format!  Enter something like A3 or D25."
        else:
            col = ord(move[0]) - ord('A')
            row = int(move[1:])-1
            if (isLegalMove(board, player, row, col) == False):
                print "That is not a legal move!  Try again."
            else:
                return (row, col)            

#helper function for getLegalMoves, returns move tuple if move exists
def getMoveFromCellInDirection(board, player, startRow, startCol, dir):
    (rows, cols) = (len(board), len(board[0]))
    dirs = [ (-1, -1), (-1, 0), (-1, +1),
             ( 0, -1),          ( 0, +1),
             (+1, -1), (+1, 0), (+1, +1) ]
    (drow,dcol) = dirs[dir]
    i = 1
    if (board[startRow][startCol] != 0):
        return []
    while True:
        row = startRow + i*drow
        col = startCol + i*dcol
        if (row < 0):
            row += rows
        if (col < 0):
            col += cols
        if (row >= rows):
            row -= rows
        if (col >= cols):
            col -= cols
            
        if (board[row][col] == 0):
            # no blanks allowed in a sandwich!
            break
        elif (board[row][col] == player):
            if i==1:
                break
            else:
            # we found the other side of the 'sandwich'
                return [(startRow,startCol)]
        else:
            # we found more 'meat' in the sandwich
            i += 1
    return []

#Prints list of moves (in tuples) for a player
def getLegalMoves(board,player):
    (rows,cols) = (len(board),len(board[0]))
    moves = []
    for r in xrange(rows):
        for c in xrange(cols):
            for dir in xrange(8):
                moves += getMoveFromCellInDirection(board,player,r,c,dir)
    return sorted(moves)

def playOthello(rows, cols):
    # create initial board
    board = make2dList(rows, cols)
    board[rows/2][cols/2] = board[rows/2-1][cols/2-1] = 1
    board[rows/2-1][cols/2] = board[rows/2][cols/2-1] = 2
    (currentPlayer, otherPlayer) = (1, 2)
    # and play until the game is over
    while True:
        if (hasMove(board, currentPlayer) == False):
            if (hasMove(board, otherPlayer)):
                print "No legal move!  PASS!"
                (currentPlayer, otherPlayer) = (otherPlayer, currentPlayer)
            else:
                print "No more legal moves for either player!  Game over!"
                break
        (row, col) = getMove(board, currentPlayer)
        makeMove(board, currentPlayer, row, col)
        player1 = 0
        player2 = 0
        for r in xrange(rows):
            for c in xrange(cols):
                if board[r][c] == 1:
                    player1 += 1
                if board[r][c] == 2:
                    player2 += 1
        print "Player X Score: ", player1
        print "Player O Score: ", player2
        (currentPlayer, otherPlayer) = (otherPlayer, currentPlayer)
    print "Goodbye!"


import random

def playOthelloAgainstRandomComputer(rows, cols):
    compRow = -1
    compCol = -1
    # create initial board
    board = make2dList(rows, cols)
    board[rows/2][cols/2] = board[rows/2-1][cols/2-1] = 1
    board[rows/2-1][cols/2] = board[rows/2][cols/2-1] = 2
    (currentPlayer, otherPlayer) = (1, 2)
    # and play until the game is over
    while True:
        if (hasMove(board, currentPlayer) == False):
            if (hasMove(board, otherPlayer)):
                print "No legal move!  PASS!"
                (currentPlayer, otherPlayer) = (otherPlayer, currentPlayer)
            else:
                print "No more legal moves for either player!  Game over!"
                break

        if (currentPlayer == 1):
            (row, col) = getMove(board, 1)
            makeMove(board, 1, row, col)
        else:
            while (isLegalMove(board,2,compRow,compCol) == False):
                compRow = random.randint(0,len(board)-1)
                compCol = random.randint(0,len(board)-1)
                print (compRow,compCol)
            makeMove(board, 2, compRow, compCol)
        
        player1 = 0
        computer = 0
        for r in xrange(rows):
            for c in xrange(cols):
                if board[r][c] == 1:
                    player1 += 1
                if board[r][c] == 2:
                    computer += 1
        print "Player X Score: ", player1
        print "Player O Score(Computer): ", computer
        
        (currentPlayer, otherPlayer) = (otherPlayer, currentPlayer)
            
    print "Goodbye!"

playOthello(10,10)
