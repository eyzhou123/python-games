def playIsola():
    board = make2dList(7,7) #Isola is played on a 7x7 board
    (rows,cols) = (7,7)
    board[0][3] = 1
    board[6][3] = 2
    (currentPlayer,otherPlayer) = (1,2)
    while True:
        for r in xrange(rows):
            for c in xrange(cols):
                if (board[r][c] == currentPlayer):
                    (row,col) = (r,c)
        if (hasMove(board,currentPlayer,row,col) == False):
            print "No more moves! Player " + getPlayerLabel(currentPlayer
            )+" loses :("
            break
        (prevRow,prevCol) = (row,col)
        (newLocation,removePiece) = getMove(board,currentPlayer)
        makeMove(board,currentPlayer,prevRow,prevCol,newLocation,removePiece)
        (currentPlayer, otherPlayer) = (otherPlayer, currentPlayer)
    print "GAMEOVER!"


def make2dList(rows, cols): #From Othello notes
    a=[]
    for row in xrange(rows): a += [[0]*cols]
    return a

#"-" means available empty piece, "." means removed piece
#"X" player 1, "O" player 2
def getPlayerLabel(player):
    labels = ["-", "X", "O","."] 
    return labels[player]

def printColLabels(board): #From Othello notes
    (rows, cols) = (7,7)
    print "  ", # skip row label
    for col in xrange(cols): print chr(ord("A")+col),
    print

def printBoard(board,currentPlayer): #From Othello notes
    (rows, cols) = (7,7)
    printColLabels(board)
    for row in xrange(rows):
        print "%2d" % (row+1),
        for col in xrange(cols): #check each piece on board
            print getPlayerLabel(board[row][col]),
        print "%2d" % (row+1)
    printColLabels(board)

def hasMove(board,player,row,col):
    for dir in xrange(8):
        if (hasMoveFromCell(board,player,row,col)):
            return True
    return False

def hasMoveFromCell(board, player, row, col): #From Othello notes
    (rows, cols) = (7,7)
    for dir in xrange(8): #check each direction, 8 directions
        if (hasMoveFromCellInDirection(board, player, row, col, dir)):
            return True
    return False

def hasMoveFromCellInDirection(board,player,row,col,dir):
    (rows,cols) = (7,7)
    dirs = [ (-1, -1), (-1, 0), (-1, +1),
             ( 0, -1),          ( 0, +1),
             (+1, -1), (+1, 0), (+1, +1) ]
    (drow,dcol) = dirs[dir]
    i = 1
    while True:
        checkRow = row + i*drow
        checkCol = col + i*dcol
        if ((checkRow < 0) or (checkRow >= rows) or (checkCol < 0
            ) or (checkCol >= cols)):
            return False
        elif (board[checkRow][checkCol] == 3): #removed piece
            return False
        elif (board[checkRow][checkCol] == 0): #blank piece
            break
        else: #other player
            return False
    return True

def getMove(board,player): #From Othello notes
    printBoard(board,player)
    #ask for (row,col)
    newLocation = 0
    removePiece = 0
    while True:
        prompt = "Enter move for player " + getPlayerLabel(player) + ": "
        move = raw_input(prompt).upper()
        # move is something like "A3"
        if ((len(move) != 2) or (not move[0].isalpha()) or (not move[1].isdigit())):
            print "Wrong format!  Enter something like A3 or D5."
        else:
            col = ord(move[0]) - ord('A')
            row = int(move[1])-1
            if (not isLegalMove(board, player, row, col)):
                print "That is not a legal move!  Try again."
            else:
                newLocation = (row, col)
                break
    while True:
        prompt = "Enter piece to remove: "
        move = raw_input(prompt).upper()
        # move is something like "A3"
        if ((len(move) != 2) or (not move[0].isalpha()) or (not move[1].isdigit())):
            print "Wrong format!  Enter something like A3 or D5."
        else:
            removeCol = ord(move[0]) - ord('A')
            removeRow = int(move[1])-1
            if (not board[row][col] == 0):
                print "That is not a legal move!  Try again."
            else:
                removePiece = (removeRow, removeCol)
                break
    return newLocation,removePiece

def isLegalMove(board, player, row, col):
    (rows, cols) = (7,7)
    if ((row < 0) or (row >= rows) or (col < 0) or (col >= cols)): return False
    return isAdjacent(board, player, row, col)

#check if this space is adjacent to previous location
def isAdjacent(board,player,row,col):
    for dir in xrange(8):
        if (isPlayersPiece(board,player,row,col,dir)):
            return True
    return False

def isPlayersPiece(board,player,row,col,dir):
    (rows,cols) = (7,7)
    dirs = [ (-1, -1), (-1, 0), (-1, +1),
             ( 0, -1),          ( 0, +1),
             (+1, -1), (+1, 0), (+1, +1) ]
    (drow,dcol) = dirs[dir]
    i = 1
    while True:
        checkRow = row + i*drow
        checkCol = col + i*dcol
        if ((checkRow < 0) or (checkRow >= rows) or (checkCol < 0
            ) or (checkCol >= cols)):
            return False
        elif (board[checkRow][checkCol] == 3): #removed space
            return False
        elif (board[checkRow][checkCol] == player): #blank space
            break
        elif (board[checkRow][checkCol] == 0): #blank space
            return False
        else: #other player
            return False
    return True

def makeMove(board,player,prevRow,prevCol,newLocation,removePiece):
    #original space becomes blank
    #new space becomes player
    (row,col) = newLocation
    (remRow,remCol) = removePiece
    board[prevRow][prevCol] = 0
    board[row][col] = player
    board[remRow][remCol] = 3
    
    
