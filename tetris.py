#tetris.py

from Tkinter import *
import random

def tetrisMousePressed(canvas,event):
    tetrisRedrawAll(canvas)

def tetrisKeyPressed(canvas,event):
    if event.keysym == "r":
        tetrisInit(canvas)
    if (canvas.data.isTetrisGameOver == False):
        if event.keysym == "Left":
            moveFallingPiece(canvas,0,-1)
        elif event.keysym == "Right":
            moveFallingPiece(canvas,0,+1)
        elif event.keysym == "Up":
            rotateFallingPiece(canvas)
        elif event.keysym == "Down":
            moveFallingPiece(canvas,+1,0)
    tetrisRedrawAll(canvas)

def tetrisTimerFired(canvas):
    if (canvas.data.isTetrisGameOver == False):
        if moveFallingPiece(canvas,+1,0) == True:
            moveFallingPiece(canvas,+1,0)
        else:
            placeFallingPiece(canvas)
            newFallingPiece(canvas)
            removeFullRows(canvas)
            if (fallingPieceIsLegal(canvas) == False):
                tetrisGameOver(canvas)
        tetrisRedrawAll(canvas)
    delay = 350 # milliseconds
    def f():
        tetrisTimerFired(canvas)
    canvas.after(delay, f)# pause, then call timerFired again

def tetrisGameOver(canvas):
    canvas.data.isTetrisGameOver = True

def tetrisRedrawAll(canvas):
    canvas.delete(ALL)
    drawTetrisGame(canvas)
    drawTetrisScore(canvas)
    if (canvas.data.isTetrisGameOver == True):
        canvas.create_text(canvas.data.width/2,
        canvas.data.height/2,text="Game Over!",font=("Helvetica",
        32, "bold"))

def loadTetrisBoard(canvas):
    (rows,cols) = (canvas.data.rows,canvas.data.cols)
    canvas.data.tetrisBoard = [([canvas.data.emptyColor]*cols) for
        row in xrange(rows)]
    
def drawTetrisGame(canvas):
    canvas.create_rectangle(0,0,canvas.data.width,canvas.data.height,
        fill = "orange")
    drawTetrisBoard(canvas)
    drawFallingPiece(canvas)

def drawTetrisBoard(canvas):
    tetrisBoard = canvas.data.tetrisBoard
    (rows,cols) = (len(tetrisBoard),len(tetrisBoard[0]))
    for row in xrange(rows):
        for col in xrange(cols):
            color = tetrisBoard[row][col]
            drawTetrisCell(canvas,row,col,color)

def drawTetrisCell(canvas,row,col,color):
    tetrisBoard = canvas.data.tetrisBoard
    margin = canvas.data.margin
    cellSize = canvas.data.cellSize
    left = margin + col * cellSize
    right = left + cellSize
    top = margin + row * cellSize
    bottom = top + cellSize
    canvas.create_rectangle(left, top, right, bottom,
        fill = "black")
    canvas.create_rectangle(left+1,top+1,right-1,bottom-1, #thin outline, use 1
        fill = color)


def drawFallingPiece(canvas):
    tetrisBoard = canvas.data.tetrisBoard
    canvas.data.fallingPieceRows = len(canvas.data.fallingPiece)
    canvas.data.fallingPieceCols = len(canvas.data.fallingPiece[0])
    for row in xrange(canvas.data.fallingPieceRow,
        canvas.data.fallingPieceRow + canvas.data.fallingPieceRows):
        for col in xrange(canvas.data.fallingPieceCol,
            canvas.data.fallingPieceCol + canvas.data.fallingPieceCols):
            if (canvas.data.fallingPiece[row-canvas.data.fallingPieceRow
                ][col-canvas.data.fallingPieceCol] == True):
                drawTetrisCell(canvas,row,col,canvas.data.fallingPieceColor)

def newFallingPiece(canvas):
    i = random.randint(0,len(canvas.data.tetrisPieces)-1)
    canvas.data.fallingPiece = canvas.data.tetrisPieces[i]
    canvas.data.fallingPieceColor = canvas.data.tetrisPieceColors[i]
    canvas.data.fallingPieceRow = 0
    canvas.data.fallingPieceCol = (canvas.data.cols/2 -
        canvas.data.fallingPieceWidth/2)

    
def moveFallingPiece(canvas,drow,dcol):
    canvas.data.fallingPieceRow += drow
    canvas.data.fallingPieceCol += dcol
    if (fallingPieceIsLegal(canvas) == False):
        canvas.data.fallingPieceRow -= drow
        canvas.data.fallingPieceCol -= dcol
        return False
    return True

def rotateFallingPiece(canvas):
    fallingPiece = canvas.data.fallingPiece
    (fallingPieceRow,fallingPieceCol) = (canvas.data.fallingPieceRow,
        canvas.data.fallingPieceCol)
    (fallingPieceRows,fallingPieceCols) = (canvas.data.fallingPieceRows,
        canvas.data.fallingPieceCols)
    
    (oldCenterRow,oldCenterCol) = fallingPieceCenter(canvas)
    (canvas.data.fallingPieceRows,canvas.data.fallingPieceCols) = (
        canvas.data.fallingPieceCols,canvas.data.fallingPieceRows)
    (newCenterRow,newCenterCol) = fallingPieceCenter(canvas)
    canvas.data.fallingPieceRow +=oldCenterRow - newCenterRow
    canvas.data.fallingPieceCol += oldCenterCol - newCenterCol

    newCols = []
    newList = []
    for row in xrange(canvas.data.fallingPieceRows):
        newCols = []
        for col in xrange(canvas.data.fallingPieceCols):
            newCols += [canvas.data.fallingPiece[
                canvas.data.fallingPieceCols-1-col][row]]
        newList += [newCols]
    canvas.data.fallingPiece = newList
    if (fallingPieceIsLegal(canvas) == False):
        canvas.data.fallingPieceRow = fallingPieceRow
        canvas.data.fallingPieceCol = fallingPieceCol
        canvas.data.fallingPieceRows = fallingPieceRows
        canvas.data.fallingPieceCols = fallingPieceCols
        canvas.data.fallingPiece = fallingPiece
    

def fallingPieceCenter(canvas):
    centerRow = canvas.data.fallingPieceRow + canvas.data.fallingPieceRows/2
    centerCol = canvas.data.fallingPieceCol + canvas.data.fallingPieceCols/2
    return (centerRow,centerCol)

def fallingPieceIsLegal(canvas):
    tetrisBoard = canvas.data.tetrisBoard
    canvas.data.fallingPieceRows = len(canvas.data.fallingPiece)
    canvas.data.fallingPieceCols = len(canvas.data.fallingPiece[0])
    for row in xrange(canvas.data.fallingPieceRow,
        canvas.data.fallingPieceRow + canvas.data.fallingPieceRows):
        for col in xrange(canvas.data.fallingPieceCol,
            canvas.data.fallingPieceCol + canvas.data.fallingPieceCols):
            if (canvas.data.fallingPiece[row-canvas.data.fallingPieceRow
                ][col-canvas.data.fallingPieceCol] == True):
                if ((row<0) or (row >= canvas.data.rows) or (col<0) or
                    (col >= canvas.data.cols) or (tetrisBoard[row][col]!=
                    canvas.data.emptyColor)):
                    return False
    return True

def placeFallingPiece(canvas):
    tetrisBoard = canvas.data.tetrisBoard
    canvas.data.fallingPieceRows = len(canvas.data.fallingPiece)
    canvas.data.fallingPieceCols = len(canvas.data.fallingPiece[0])
    for row in xrange(canvas.data.fallingPieceRow,
        canvas.data.fallingPieceRow + canvas.data.fallingPieceRows):
        for col in xrange(canvas.data.fallingPieceCol,
            canvas.data.fallingPieceCol + canvas.data.fallingPieceCols):
            if (canvas.data.fallingPiece[row-canvas.data.fallingPieceRow
                ][col-canvas.data.fallingPieceCol] == True):
                tetrisBoard[row][col] = canvas.data.fallingPieceColor

def removeFullRows(canvas):
    tetrisBoard = canvas.data.tetrisBoard
    fullRows = 0
    newRow = canvas.data.rows-1
    for oldRow in xrange(canvas.data.rows-1,-1,-1):
        if (canvas.data.emptyColor in tetrisBoard[oldRow]):
            for col in xrange(canvas.data.cols):
                tetrisBoard[newRow][col] = tetrisBoard[oldRow][col] 
            newRow -= 1
        else:
            fullRows += 1
            canvas.data.score += fullRows**2

def drawTetrisScore(canvas):
    canvas.create_text(canvas.data.cellSize,canvas.data.cellSize/2,
        text="Score: " + str(canvas.data.score),anchor=W,
        font=("Helvetica",16, "bold"))

def tetrisInit(canvas):
    canvas.data.emptyColor = "blue"
    loadTetrisBoard(canvas)
    canvas.data.iPiece = [
    [ True,  True,  True,  True]
    ]
    canvas.data.jPiece = [
    [ True, False, False ],
    [ True, True,  True]
    ]
    canvas.data.lPiece = [
    [ False, False, True],
    [ True,  True,  True]
    ]
    canvas.data.oPiece = [
    [ True, True],
    [ True, True]
    ]
    canvas.data.sPiece = [
    [ False, True, True],
    [ True,  True, False ]
    ]
    canvas.data.tPiece = [
    [ False, True, False ],
    [ True,  True, True]
    ]
    canvas.data.zPiece = [
    [ True,  True, False ],
    [ False, True, True]
    ]
    canvas.data.tetrisPieces = [canvas.data.iPiece, canvas.data.jPiece,
        canvas.data.lPiece, canvas.data.oPiece,canvas.data.sPiece,
        canvas.data.tPiece, canvas.data.zPiece ]
    canvas.data.tetrisPieceColors = [ "red", "yellow", "magenta",
        "pink", "cyan", "green", "orange" ]
    canvas.data.fallingPiece = canvas.data.tetrisPieces[
    random.randint(0,len(canvas.data.tetrisPieces)-1)]
    canvas.data.fallingPieceColor = canvas.data.tetrisPieceColors[
    canvas.data.tetrisPieces.index(canvas.data.fallingPiece)]
    canvas.data.fallingPieceRow = 0
    canvas.data.fallingPieceWidth = len(canvas.data.fallingPiece[0])
    canvas.data.fallingPieceCol = (canvas.data.cols/2 -
    canvas.data.fallingPieceWidth/2)
    canvas.data.fallingPieceRows = len(canvas.data.fallingPiece)
    canvas.data.fallingPieceCols = len(canvas.data.fallingPiece[0])
    canvas.data.isTetrisGameOver = False
    canvas.data.score = 0
    tetrisRedrawAll(canvas)

def tetrisRun(rows,cols):
    # create the root and the canvas
    root = Tk()
    margin = 30
    cellSize = 30
    canvasWidth = 2*margin + cols*cellSize
    canvasHeight = 2*margin + rows*cellSize
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    root.resizable(width=0, height=0)
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.margin = margin
    canvas.data.cellSize = cellSize
    canvas.data.rows = rows
    canvas.data.cols = cols
    canvas.data.width = canvasWidth
    canvas.data.height = canvasHeight
    tetrisInit(canvas)
    # set up events
    def f(event): tetrisMousePressed(canvas, event)    
    root.bind("<Button-1>", f)
    def g(event): tetrisKeyPressed(canvas, event)    
    root.bind("<Key>", g)
    tetrisTimerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

tetrisRun(15,10)
