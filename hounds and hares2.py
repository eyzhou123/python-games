#hounds and hares.py

from Tkinter import *

def hAHMousePressed(canvas,event):
    (rows,cols) = (canvas.data.rows,canvas.data.cols)
    margin = canvas.data.margin
    cellSize = canvas.data.cellSize
    if (canvas.data.isHAHRoundOver == True): #click before new round starts
        hAHInit(canvas)
    if (canvas.data.isHAHGameOver == False):
        if (canvas.data.currPlayer == "Hound" and canvas.data.houndChoiceMade
        == False and (canvas.data.isLegalCol == False or
        canvas.data.isLegalRow == False)):

            for c in xrange(cols):
                if (margin + (margin+cellSize)*c <= event.x <=
                cellSize+margin + (margin+cellSize)*c):
                    canvas.data.houndCol = c
                    canvas.data.isLegalCol = True
            for r in xrange(rows):
                if (margin + (margin+cellSize)*r <= event.y <=
                cellSize+margin + (margin+cellSize)*r):
                    canvas.data.houndRow = r
                    canvas.data.isLegalRow = True
            if (canvas.data.isLegalCol == True and canvas.data.isLegalRow
            == True):
                #reset isLegalRow and isLegalCol
                canvas.data.isLegalCol = False
                canvas.data.isLegalRow = False
                if ((0 <= canvas.data.houndRow <= rows - 1) and (0 <=
                    canvas.data.houndCol <= cols - 1) and
                    (canvas.data.hAHBoard[canvas.data.houndRow][
                    canvas.data.houndCol] not in canvas.data.emptyCorners)):
                        canvas.data.houndToMove = canvas.data.hAHBoard[
                        canvas.data.houndRow][canvas.data.houndCol]
                if (canvas.data.houndToMove >= 1):
                    canvas.data.houndChoiceMade = True
                elif (canvas.data.houndToMove < 1):
                    print "That is not an option. Try again."
            else:
                print "Be sure to click on the circles."              
        elif ((canvas.data.currPlayer=="Hound" and
        canvas.data.houndChoiceMade==True and (canvas.data.isLegalCol ==
        False or canvas.data.isLegalRow == False))):

            for c in xrange(cols):
                if (margin + (margin+cellSize)*c <= event.x <=
                cellSize+margin + (margin+cellSize)*c):
                    canvas.data.houndMoveCol = c
                    canvas.data.isLegalCol = True
            for r in xrange(rows):
                if (margin + (margin+cellSize)*r <= event.y <=
                cellSize+margin + (margin+cellSize)*r):
                    canvas.data.houndMoveRow = r
                    canvas.data.isLegalRow = True
            if (canvas.data.isLegalCol == True and canvas.data.isLegalRow
            == True):
                #reset isLegalRow and isLegalCol
                canvas.data.isLegalCol = False
                canvas.data.isLegalRow = False
                if ((0 <= canvas.data.houndMoveRow <= rows - 1) and (0 <=
                    canvas.data.houndMoveCol <= cols - 1) and
                    canvas.data.hAHBoard[canvas.data.houndMoveRow][
                    canvas.data.houndMoveCol] == 0 and isLegalHoundMove(canvas,
                    canvas.data.houndToMove,canvas.data.houndMoveRow,
                    canvas.data.houndMoveCol)):
                        canvas.data.houndMoveMade = True
                        canvas.data.time = 0
                        moveHound(canvas,canvas.data.houndToMove,
                        canvas.data.houndMoveRow,canvas.data.houndMoveCol)
                        #check for only case when hound wins
                        if not existsLegalHareMove(canvas):
                            canvas.data.roundWinner = "Hound"
                            canvas.data.p1Wins += 1
                            hAHRoundOver(canvas)
                        else:
                            #switch players
                            (canvas.data.currPlayer,canvas.data.othPlayer)=(
                                canvas.data.othPlayer,canvas.data.currPlayer)
                            canvas.data.houndChoiceMade = False #reset
                            canvas.data.houndMoveMade = False
                else: 
                    print "That location is not available. Try again."
            else:
                print "Be sure to click on the circles."

        elif (canvas.data.currPlayer == "Hare" and
        canvas.data.hareMoveMade == False and (canvas.data.isLegalCol ==
        False or canvas.data.isLegalRow == False)):

            for c in xrange(cols):
                if (margin + (margin+cellSize)*c <= event.x <=
                cellSize+margin + (margin+cellSize)*c):
                    canvas.data.hareMoveCol = c
                    canvas.data.isLegalCol = True
            for r in xrange(rows):
                if (margin + (margin+cellSize)*r <= event.y <=
                cellSize+margin + (margin+cellSize)*r):
                    canvas.data.hareMoveRow = r
                    canvas.data.isLegalRow = True
            if (canvas.data.isLegalCol == True and canvas.data.isLegalRow
            == True):
                #reset isLegalRow and isLegalCol
                canvas.data.isLegalCol = False
                canvas.data.isLegalRow = False
                if ((0 <= canvas.data.hareMoveRow <= rows - 1) and (0 <=
                    canvas.data.hareMoveCol <= cols - 1)and
                    canvas.data.hAHBoard[canvas.data.hareMoveRow][
                    canvas.data.hareMoveCol] == 0 and isLegalHareMove(canvas,
                    canvas.data.hareMoveRow,canvas.data.hareMoveCol)):
                        canvas.data.hareMoveMade = True
                        canvas.data.time = 0
                        moveHare(canvas,canvas.data.hareMoveRow,
                        canvas.data.hareMoveCol)
                        #switch players
                        (canvas.data.currPlayer,canvas.data.othPlayer)=(
                            canvas.data.othPlayer,canvas.data.currPlayer)
                        canvas.data.hareMoveMade = False #reset
                else: 
                    print "That location is not available. Try again."
            else:
                print "Be sure to click on the circles."
    hAHRedrawAll(canvas)

def existsLegalHareMove(canvas):
    (rows,cols) = (canvas.data.rows,canvas.data.cols)
    #check all the adjacent spots
    for row in xrange(canvas.data.hareRow-1,canvas.data.hareRow+1+1): 
        for col in xrange(canvas.data.hareCol-1,canvas.data.hareCol+1+1):
            if ((0 <= row <= rows - 1) and (0 <= col <= cols - 1)):
                if (canvas.data.hAHBoard[row][col] == 0 and
                isLegalHareMove(canvas,row,col)):
                    return True
    return False               

def hAHKeyPressed(canvas,event):
    hAHRedrawAll(canvas)

def hAHTimerFired(canvas):
    if (canvas.data.isHAHGameOver == False):
        if (canvas.data.isHAHRoundOver == False):
            print canvas.data.time
            canvas.data.time += 1
            if (canvas.data.houndChoiceMade == False or
            canvas.data.houndMoveMade == False or
            canvas.data.hareMoveMade == False):
                #we will flash the blank screen twice to be noticeable
                if (canvas.data.time == canvas.data.maxSecondsPerTurn):
                    timesUp(canvas)
                if (canvas.data.time == canvas.data.maxSecondsPerTurn +
                canvas.data.flashLength):
                    canvas.data.isTimesUp = False
                if (canvas.data.time == canvas.data.maxSecondsPerTurn +
                    2*canvas.data.flashLength):
                    timesUp(canvas)
                if (canvas.data.time == canvas.data.maxSecondsPerTurn +
                    3*canvas.data.flashLength): 
                    canvas.data.isTimesUp = False
                    (canvas.data.currPlayer,canvas.data.othPlayer) = (
                    canvas.data.othPlayer,canvas.data.currPlayer) #pass turn
                    canvas.data.time = 0 #restart timer
        hAHRedrawAll(canvas)
    delay = 250 
    def f():
        hAHTimerFired(canvas)
    canvas.after(delay, f) # pause, then call timerFired again

def hAHRedrawAll(canvas):
    canvas.delete(ALL)
    drawHAHBoard(canvas)
    drawHound1(canvas)
    drawHound2(canvas)
    drawHound3(canvas)
    drawHare(canvas)
    drawP1Score(canvas)
    drawP2Score(canvas)
    drawIndicateTurn(canvas)
    if (canvas.data.currPlayer == "Hound" and canvas.data.houndChoiceMade
    == True):
        drawHoundHighlight(canvas)
    if (canvas.data.isTimesUp == True):
        canvas.create_rectangle(0,0,canvas.data.width,canvas.data.height,
        fill = "white")
    elif (canvas.data.isHAHGameOver == True):
        canvas.create_text(canvas.data.width/2, canvas.data.height/2,
        text="Game Over! " + canvas.data.gameWinner +" wins!",font=("Helvetica",
        32, "bold"))
    elif (canvas.data.isHAHRoundOver == True):
        canvas.create_text(canvas.data.width/2, canvas.data.height/2,
        text="Round Over! " + canvas.data.roundWinner + " wins round!",font=(
        "Helvetica",32, "bold"))


def drawHoundHighlight(canvas):
    houndNum = canvas.data.houndToMove
    if (canvas.data.houndToMove == 1):
        (row,col) = (canvas.data.hound1Row,canvas.data.hound1Col)
    elif (canvas.data.houndToMove == 2):
        (row,col) = (canvas.data.hound2Row,canvas.data.hound2Col)
    else:
        (row,col) = (canvas.data.hound3Row,canvas.data.hound3Col)
    margin = canvas.data.margin
    cellSize = canvas.data.cellSize
    left = margin + col * (cellSize + margin)
    right = left + cellSize
    top = margin + row * (cellSize + margin)
    bottom = top + cellSize
    canvas.create_oval(left, top, right, bottom, fill="red", width = 5)

def timesUp(canvas):
    canvas.data.isTimesUp = True
    hAHRedrawAll(canvas)

def drawP1Score(canvas):
    canvas.create_text(0, canvas.data.height,
    text="Score: " + str(canvas.data.p1Wins),anchor = SW,
    font=("Helvetica",14, "bold"))

def drawP2Score(canvas):
    canvas.create_text(canvas.data.width, canvas.data.height,
    text="Score: " + str(canvas.data.p2Wins),anchor = SE,
    font=("Helvetica",14, "bold"))

def moveHound(canvas,houndNum,row,col):
    hAHBoard = canvas.data.hAHBoard
    #for all hounds, first reset verticalCount if not vertical movement
    #check for vertical movement
    #check for hare win
    if (houndNum == 1):
        if ((canvas.data.hound1Row,canvas.data.hound1Col) != (row-1,col) and
        (canvas.data.hound1Row,canvas.data.hound1Col) != (row+1,col)):
            canvas.data.verticalCount = 0
        if ((canvas.data.hound1Row,canvas.data.hound1Col) == (row-1,col) or
        (canvas.data.hound1Row,canvas.data.hound1Col) == (row+1,col)):
            canvas.data.verticalCount += 1
        hAHBoard[canvas.data.hound1Row][canvas.data.hound1Col] = 0
        hAHBoard[row][col] = 1
        (canvas.data.hound1Row, canvas.data.hound1Col) = (row,col)
    elif (houndNum == 2):
        if ((canvas.data.hound2Row,canvas.data.hound2Col) != (row-1,col) and
        (canvas.data.hound2Row,canvas.data.hound2Col) != (row+1,col)):
            canvas.data.verticalCount = 0
        if ((canvas.data.hound2Row,canvas.data.hound2Col) == (row-1,col) or
        (canvas.data.hound2Row,canvas.data.hound2Col) == (row+1,col)):
            canvas.data.verticalCount += 1
        hAHBoard[canvas.data.hound2Row][canvas.data.hound2Col] = 0
        hAHBoard[row][col] = 2
        (canvas.data.hound2Row, canvas.data.hound2Col) = (row,col)
    else:
        if ((canvas.data.hound3Row,canvas.data.hound3Col) != (row-1,col) and
        (canvas.data.hound3Row,canvas.data.hound3Col) != (row+1,col)):
            canvas.data.verticalCount = 0
        if ((canvas.data.hound3Row,canvas.data.hound3Col) == (row-1,col) or
        (canvas.data.hound3Row,canvas.data.hound3Col) == (row+1,col)):
            canvas.data.verticalCount += 1
        hAHBoard[canvas.data.hound3Row][canvas.data.hound3Col] = 0
        hAHBoard[row][col] = 3
        (canvas.data.hound3Row, canvas.data.hound3Col) = (row,col)
    #case where hounds are stalling
    if (canvas.data.verticalCount == 10):
        canvas.data.roundWinner = "Hare"
        canvas.data.p2Wins += 1
        hAHRoundOver(canvas)
    #case where hare has reached the other side
    if (canvas.data.hareCol == 0):
        canvas.data.roundWinner = "Hare"
        canvas.data.p2Wins += 1
        hAHRoundOver(canvas)
    #case where hare is behind/to the left of all hounds       
    if ((canvas.data.hareCol < canvas.data.hound1Col) and
        (canvas.data.hareCol < canvas.data.hound2Col) and
        (canvas.data.hareCol < canvas.data.hound3Col)):
        canvas.data.roundWinner = "Hare"
        canvas.data.p2Wins += 1
        hAHRoundOver(canvas)

#replace old position with 0, make new spot -1 (hare)
#check for hare win
def moveHare(canvas,row,col):
    hAHBoard = canvas.data.hAHBoard
    hAHBoard[canvas.data.hareRow][canvas.data.hareCol] = 0
    hAHBoard[row][col] = -1
    (canvas.data.hareRow, canvas.data.hareCol) = (row,col)
    #case where hare has reached the other side
    if (canvas.data.hareCol == 0):
        canvas.data.roundWinner = "Hare"
        canvas.data.p2Wins += 1
        hAHRoundOver(canvas)
    #case where hare is behind/to the left of all hounds
    if ((canvas.data.hareCol < canvas.data.hound1Col) and
        (canvas.data.hareCol < canvas.data.hound2Col) and
        (canvas.data.hareCol < canvas.data.hound3Col)):
        canvas.data.roundWinner = "Hare"
        canvas.data.p2Wins += 1
        hAHRoundOver(canvas)

def isLegalHoundMove(canvas,houndNum,row,col):
    (rows,cols) = (canvas.data.rows,canvas.data.cols)
    if (houndNum == 1):
        (oldRow,oldCol) = (canvas.data.hound1Row,canvas.data.hound1Col)
    elif (houndNum == 2):
        (oldRow,oldCol) = (canvas.data.hound2Row,canvas.data.hound2Col)
    else:
        (oldRow,oldCol) = (canvas.data.hound3Row,canvas.data.hound3Col)
    #Go by different cases, like in drawHAHBoard
    #We don't use elif here because some conditions are the same (we should
    #not exclude cases
    if ((((row%2 == 1) and (col%2 ==0)) or ((row%2 == 0) and (
    col%2 == 1))) and (row != 0) and (col != 0)):
        if ((row,col) == (oldRow+1,oldCol+1)): #diagonal down
            return True
        
    if ((((row%2 == 1) and (col%2 ==0)) or ((row%2 == 0) and (
    col%2 == 1))) and (row != rows-1) and (col != 0)):
        if ((row,col) == (oldRow-1,oldCol+1)): #diagonal up
            return True
        
    if (((0 < col < cols-1) and (row != 0)) or ((col == 0) and (row != 0))
        or ((col == cols -1) and (row != 0))):
        if ((row,col) == (oldRow+1,oldCol)): #down
            return True
        
    if (((0 < col < cols-1) and (row != rows-1)) or ((col == 0) and
        (row != rows - 1)) or ((col == cols -1) and (row != rows - 1))):
        if ((row,col) == (oldRow-1,oldCol)): #up
            return True
        
    if (((col != 0) and ((row != 0) and (row != rows - 1)))
    or ((row == 0) and (1 < col)) or ((row == rows - 1)
    and (1 < col))):
        if ((row,col) == (oldRow,oldCol+1)): #right
            return True
        
    #Any backwards movement for hounds is illegal!
    if ((row,col) == (oldRow,oldCol-1) or (row,col) == (oldRow-1,oldCol-1)
    or (row,col) == (oldRow+1,oldCol-1)):
        return False
    return False

def isLegalHareMove(canvas,row,col):
    #Go by different cases, like in drawHAHBoard
    #More directions here because the hare can go backwards
    #We don't use elif here because some conditions are the same (we should
    #not exclude cases
    (rows,cols) = (canvas.data.rows,canvas.data.cols)
    (oldRow,oldCol) = (canvas.data.hareRow,canvas.data.hareCol)
    if ((((row%2 == 1) and (col%2 ==0)) or ((row%2 == 0) and (
    col%2 == 1))) and (row != rows-1) and (col != 0)):
        if ((row,col) == (oldRow+1,oldCol+1)): #diagonal down right
            return True
        
    if ((((row%2 == 1) and (col%2 ==0)) or ((row%2 == 0) and (
    col%2 == 1))) and (row != 0) and (col != cols-1)):
        if ((row,col) == (oldRow+1,oldCol-1)): #diagonal down left
            return True
        
    if ((((row%2 == 1) and (col%2 ==0)) or ((row%2 == 0) and (
    col%2 == 1))) and (row != 0) and (col != 0)):
        if ((row,col) == (oldRow-1,oldCol+1)): #diagonal up right
            return True
        
    if ((((row%2 == 1) and (col%2 ==0)) or ((row%2 == 0) and (
    col%2 == 1))) and (row != rows-1) and (col != cols-1)):
        if ((row,col) == (oldRow-1,oldCol-1)): #diagonal up left
            return True
        
    if (((0 < col < cols-1) and (row != 0)) or ((col == 0) and (row != 0))
        or ((col == cols -1) and (row != 0))):
        if ((row,col) == (oldRow+1,oldCol)): #down
            return True
        
    if (((0 < col < cols-1) and (row != rows-1)) or ((col == 0) and
        (row != rows - 1)) or ((col == cols -1) and (row != rows - 1))):
        if ((row,col) == (oldRow-1,oldCol)): #up
            return True
        
    if (((col != 0) and ((row != 0) and (row != rows - 1)))
    or ((row == 0) and (1 < col)) or ((row == rows - 1)
    and (1 < col))):
        if ((row,col) == (oldRow,oldCol+1)): #right
            return True
        
    if (((col != cols-1) and ((row != 0) and (row != rows - 1)))
    or ((row == 0) and (0 < col < cols - 2)) or ((row == rows - 1)
    and (0 < col < cols - 2))):
        if ((row,col) == (oldRow,oldCol-1)): #left
            return True
    return False

def hAHRoundOver(canvas):
    canvas.data.isHAHRoundOver = True
    canvas.data.rounds += 1
    if (canvas.data.p1Wins == 3):
        canvas.data.gameWinner = canvas.data.p1
        hAHGameOver(canvas)
        hAHRedrawAll(canvas)
    elif (canvas.data.p2Wins == 3):
        canvas.data.gameWinner = canvas.data.p2
        hAHGameOver(canvas)
        canvas.data.isHAHRoundOver = False
        hAHRedrawAll(canvas)
    hAHRedrawAll(canvas)
        
def hAHGameOver(canvas):
    canvas.data.isHAHGameOver = True

def drawIndicateTurn(canvas):
    if (canvas.data.currPlayer == "Hound"):
        canvas.create_text(canvas.data.width/2,0,
        text= (
        "Hound's turn! Click a hound, and then the desired location."),
        anchor=N,font=("Helvetica",14,"bold"))
    else:
        canvas.create_text(canvas.data.width/2,0,
        text= "Hare's turn! Click the desired location.",
        anchor=N,font=("Helvetica",14,"bold"))
        

def loadHAHBoard(canvas):
   (rows,cols) = (canvas.data.rows,canvas.data.cols)
   canvas.data.hAHBoard = [([0]*cols) for row in xrange(rows)]


#draw lines on the board, using patterns (such as even rows, odd cols etc.) and
#take into account different board dimensions
#draw cells
def drawHAHBoard(canvas):
    hAHBoard = canvas.data.hAHBoard
    (rows,cols) = (len(hAHBoard),len(hAHBoard[0]))
    for row in xrange(rows):
        for col in xrange(cols):
            if ((((row%2 == 1) and (col%2 ==0)) or ((row%2 == 0) and (
                col%2 == 1)) or ((row == rows - 2) and
                (col == 0)) or ((row == 0) and (col == cols - 2))) and
                 (row != rows-1) and (col != cols-1)):
                drawDiagDownLine(canvas,hAHBoard,row,col)
                
            if ((((row%2 == 1) and (col%2 ==0)) or ((row%2 == 0) and (
                col%2 == 1)) or ((row == rows - 1) and (col == cols -2) and
                (col != cols -1))) and (row != 0) and (col != cols-1)):
                drawDiagUpLine(canvas,hAHBoard,row,col)
                
            if (((0 < col < cols-1) and (row != rows - 1)) or ((rows > 3)
                and (row != rows - 2) and (col == 0 or col == cols-1))):
                drawDownLine(canvas,hAHBoard,row,col)
                
            if (((col != cols - 1) and ((row != 0) and (row != rows - 1)))
                or ((row == 0) and (0 < col < cols - 2)) or ((row == rows - 1)
                and (0 < col < cols - 2))):
                drawRightLine(canvas,hAHBoard,row,col)
    for row in xrange(rows):
        for col in xrange(cols):
            drawHAHCell(canvas,hAHBoard,row,col)

def drawDiagDownLine(canvas,hAHBoard,row,col):
    margin = canvas.data.margin
    cellSize = canvas.data.cellSize
    x1 = margin + col * (cellSize + margin) + cellSize/2
    y1 = margin + row * (cellSize + margin) + cellSize/2
    x2 = margin + (col + 1) * (cellSize + margin) + cellSize/2
    y2 = margin + (row + 1) * (cellSize + margin) + cellSize/2
    if (hAHBoard[row][col] > -2):
        canvas.create_line(x1,y1,x2,y2,fill = "black")

def drawDiagUpLine(canvas,hAHBoard,row,col):
    margin = canvas.data.margin
    cellSize = canvas.data.cellSize
    x1 = margin + col * (cellSize + margin) + cellSize/2
    y1 = margin + row * (cellSize + margin) + cellSize/2
    x2 = margin + (col + 1) * (cellSize + margin) + cellSize/2
    y2 = margin + (row - 1) * (cellSize + margin) + cellSize/2
    if (hAHBoard[row][col] > -2):
        canvas.create_line(x1,y1,x2,y2,fill = "black")
        
def drawDownLine(canvas,hAHBoard,row,col):
    margin = canvas.data.margin
    cellSize = canvas.data.cellSize
    x1 = margin + col * (cellSize + margin) + cellSize/2
    y1 = margin + row * (cellSize + margin) + cellSize/2
    x2 = margin + (col) * (cellSize + margin) + cellSize/2
    y2 = margin + (row + 1) * (cellSize + margin) + cellSize/2
    if (hAHBoard[row][col] > -2):
        canvas.create_line(x1,y1,x2,y2,fill = "black")

def drawRightLine(canvas,hAHBoard,row,col):
    margin = canvas.data.margin
    cellSize = canvas.data.cellSize
    x1 = margin + col * (cellSize + margin) + cellSize/2
    y1 = margin + row * (cellSize + margin) + cellSize/2
    x2 = margin + (col + 1) * (cellSize + margin) + cellSize/2
    y2 = margin + (row) * (cellSize + margin) + cellSize/2
    if (hAHBoard[row][col] > -2):
        canvas.create_line(x1,y1,x2,y2,fill = "black")
        
def drawHAHCell(canvas,hAHBoard,row,col):
    margin = canvas.data.margin
    cellSize = canvas.data.cellSize
    left = margin + col * (cellSize + margin)
    right = left + cellSize
    top = margin + row * (cellSize + margin)
    bottom = top + cellSize
    if (hAHBoard[row][col] == 0):
        canvas.create_oval(left, top, right, bottom, fill="white")
    elif (hAHBoard[row][col] > 0):
        canvas.create_oval(left, top, right, bottom, fill="red")
    elif (hAHBoard[row][col] == -1):
        canvas.create_oval(left, top, right, bottom, fill="blue")
        

def drawHound1(canvas):
    hAHBoard = canvas.data.hAHBoard
    (row,col) = (canvas.data.hound1Row,canvas.data.hound1Col)
    drawHAHCell(canvas,hAHBoard,row,col)
    
def drawHound2(canvas):
    hAHBoard = canvas.data.hAHBoard
    (row,col) = (canvas.data.hound2Row,canvas.data.hound2Col)
    drawHAHCell(canvas,hAHBoard,row,col)
    
def drawHound3(canvas):
    hAHBoard = canvas.data.hAHBoard
    (row,col) = (canvas.data.hound3Row,canvas.data.hound3Col)
    drawHAHCell(canvas,hAHBoard,row,col)

def drawHare(canvas):
    hAHBoard = canvas.data.hAHBoard
    (row,col) = (canvas.data.hareRow,canvas.data.hareCol)
    drawHAHCell(canvas,hAHBoard,row,col)
    
    
def hAHInit(canvas):
    loadHAHBoard(canvas)
    canvas.data.time = 0
    canvas.data.emptyCorners = [canvas.data.hAHBoard[0][0],
        canvas.data.hAHBoard[0][canvas.data.cols-1],
        canvas.data.hAHBoard[canvas.data.rows-1][0],
        canvas.data.hAHBoard[canvas.data.rows-1][canvas.data.cols-1]]
    #make empty corners = -2 (don't draw them)
    canvas.data.hAHBoard[0][0] = -2
    canvas.data.hAHBoard[0][canvas.data.cols-1] = -2
    canvas.data.hAHBoard[canvas.data.rows-1][0] = -2
    canvas.data.hAHBoard[canvas.data.rows-1][canvas.data.cols-1] = -2
    canvas.data.p1 = "Hound"
    canvas.data.p2 = "Hare"
    canvas.data.currPlayer = "Hound"
    canvas.data.othPlayer = "Hare"
    canvas.data.hound1Row = 0
    canvas.data.hound1Col = 1
    canvas.data.hound2Row = canvas.data.rows/2
    canvas.data.hound2Col = 0
    canvas.data.hound3Row = canvas.data.rows-1
    canvas.data.hound3Col = 1
    canvas.data.hareRow = canvas.data.rows/2
    canvas.data.hareCol = canvas.data.cols-1
    canvas.data.hAHBoard[canvas.data.hound1Row][canvas.data.hound1Col] = 1
    canvas.data.hAHBoard[canvas.data.hound2Row][canvas.data.hound2Col] = 2
    canvas.data.hAHBoard[canvas.data.hound3Row][canvas.data.hound3Col] = 3
    canvas.data.hAHBoard[canvas.data.hareRow][canvas.data.hareCol] = -1
    canvas.data.verticalCount = 0
    canvas.data.houndRow = -1
    canvas.data.houndCol = -1
    canvas.data.houndMoveRow = -1
    canvas.data.houndMoveCol = -1
    canvas.data.isLegalRow = False
    canvas.data.isLegalCol = False
    canvas.data.houndToMove = None
    canvas.data.houndChoiceMade = False
    canvas.data.houndMoveMade = False
    canvas.data.hareMoveMade = False
    canvas.data.isHAHGameOver = False
    canvas.data.isHAHRoundOver = False
    canvas.data.roundWinner = None
    canvas.data.gameWinner = None
    canvas.data.isTimesUp = False
    canvas.data.flashLength = 1
    hAHRedrawAll(canvas)
               

def runHareAndHounds(maxSecondsPerTurn):
    # create the root and the canvas
    root = Tk()
    rows = 3
    cols = 5
    margin = 30
    cellSize = 60
    canvasWidth = margin*(cols+1) + cols*cellSize
    canvasHeight = margin*(rows+1) + rows*cellSize
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.margin = margin
    canvas.data.cellSize = cellSize
    canvas.data.rows = rows
    canvas.data.cols = cols
    canvas.data.width = canvasWidth
    canvas.data.height = canvasHeight
    canvas.data.p1Wins = 0
    canvas.data.p2Wins = 0
    canvas.data.rounds = 0
    canvas.data.p1 = "Hound"
    canvas.data.p2 = "Hare"
    canvas.data.maxSecondsPerTurn = maxSecondsPerTurn
    hAHInit(canvas)
    # set up events
    def f(event): hAHMousePressed(canvas, event)    
    root.bind("<Button-1>", f)
    def g(event): hAHKeyPressed(canvas, event)    
    root.bind("<Key>", g)
    hAHTimerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

runHareAndHounds(30)
