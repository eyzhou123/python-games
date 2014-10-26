# snake0.py
  
from Tkinter import *
import random

def snakeMousePressed(canvas,event):
    snakeRedrawAll(canvas)

def snakeKeyPressed(canvas,event):
    canvas.data.ignoreNextTimerEvent = True
    if event.keysym == "r":
        snakeInit(canvas)
    elif event.keysym == "q":
        snakeGameOver(canvas)
    elif event.keysym == "d":
        canvas.data.inDebugMode = not canvas.data.inDebugMode
    if (canvas.data.isSnakeGameOver == False):
        if event.keysym == "Left":
            moveSnake(canvas,0,-1)
        elif event.keysym == "Right":
            moveSnake(canvas,0,+1)
        elif event.keysym == "Up":
            moveSnake(canvas,-1,0)
        elif event.keysym == "Down":
            moveSnake(canvas,+1,0)
    snakeRedrawAll(canvas)

def snakeTimerFired(canvas):
    if canvas.data.isSnakeGameOver == False:
        (drow,dcol) = (canvas.data.snakeDRow,canvas.data.snakeDCol)
        moveSnake(canvas,drow,dcol)
        snakeRedrawAll(canvas)
    delay = 150 # milliseconds
    def f():
        snakeTimerFired(canvas)
    canvas.after(delay, f) # pause, then call timerFired again

def snakeRedrawAll(canvas):
    canvas.delete(ALL)
    drawSnakeBoard(canvas)
    if (canvas.data.isSnakeGameOver == True):
        canvas.create_text(canvas.data.canvasWidth/2, canvas.data.canvasHeight/2,
        text="Game Over!",font=("Helvetica", 32, "bold"))

def drawSnakeBoard(canvas):
    # you write this!
    # hint: for every row,col position on the board, call
    # drawSnakeCell, a helper method you will also write, like so
    #    drawSnakeCell(snakeBoard, row, col)
    (rows,cols) = (len(canvas.data.snakeBoard),len(canvas.data.snakeBoard[0]))
    for row in xrange(rows):
        for col in xrange(cols):
            drawSnakeCell(canvas,canvas.data.snakeBoard,row,col)


def drawSnakeCell(canvas,snakeBoard, row, col):
    # you write this!
    # hint: place a margin 5-pixels-wide around the board.
    # make each cell 30x30
    # draw a white square and then, if the snake is in the
    # cell, draw a blue circle.
    margin = canvas.data.margin
    cellSize = canvas.data.cellSize
    left = margin + col * cellSize
    right = left + cellSize
    top = margin + row * cellSize
    bottom = top + cellSize
    canvas.create_rectangle(left, top, right, bottom, fill="white")
    if (snakeBoard[row][col] > 0):
        # draw part of the snake body
        canvas.create_oval(left, top, right, bottom, fill="blue")
    if (snakeBoard[row][col] < 0):
        canvas.create_oval(left, top, right, bottom, fill="green")
    if (canvas.data.inDebugMode == True):
        canvas.create_text(left+cellSize/2,top+cellSize/2,
        text=str(snakeBoard[row][col]))

        
def loadSnakeBoard(canvas):
    # you write this!
    # allocate the new snakeBoard 2d list as described
    # in the notes, and store it in the canvas's data
    (rows,cols) = (canvas.data.canvasRows,canvas.data.canvasCols)
    canvas.data.snakeBoard = [([0]*cols) for row in xrange(rows)]
    canvas.data.snakeBoard[rows/2][cols/2] = 1
    canvas.data.ignoreNextTimerEvent = False
    findSnakeHead(canvas)
    snakePlaceFood(canvas)

def findSnakeHead(canvas):
    snakeBoard = canvas.data.snakeBoard
    (rows,cols) = (len(snakeBoard),len(snakeBoard[0]))
    headRow = canvas.data.headRow
    headCol = canvas.data.headCol
    for row in xrange(rows):
        for col in xrange(cols):
            if snakeBoard[row][col] > snakeBoard[headRow][headCol]:
                (headRow,headCol) = (row,col)
    (canvas.data.headRow,canvas.data.headCol) = (headRow,headCol)

def removeTail(canvas):
    snakeBoard= canvas.data.snakeBoard
    (rows,cols) = (len(snakeBoard),len(snakeBoard[0]))
    for row in xrange(rows):
        for col in xrange(cols):
            if snakeBoard[row][col]>0:
                snakeBoard[row][col] -= 1

def moveSnake(canvas,drow,dcol):
    snakeBoard = canvas.data.snakeBoard
    (rows,cols) = (len(snakeBoard),len(snakeBoard[0]))
    (canvas.data.snakeDRow,canvas.data.snakeDCol) = (drow,dcol)
    headRow = canvas.data.headRow
    headCol = canvas.data.headCol
    newHeadRow = headRow + drow
    newHeadCol = headCol + dcol
    
    if ((newHeadRow < 0 ) or (newHeadRow >= rows) or (newHeadCol < 0)
        or (newHeadCol >= cols)):
        snakeGameOver(canvas)
    elif (snakeBoard[newHeadRow][newHeadCol] > 0):
        snakeGameOver(canvas)
    elif (snakeBoard[newHeadRow][newHeadCol] < 0):
        snakeBoard[newHeadRow][newHeadCol] = 1 + snakeBoard[headRow][headCol]
        (canvas.data.headRow,canvas.data.headCol) = (newHeadRow,newHeadCol)
        snakePlaceFood(canvas)
    else:
        snakeBoard[newHeadRow][newHeadCol] = 1 + snakeBoard[headRow][headCol]
        (canvas.data.headRow,canvas.data.headCol) = (newHeadRow,newHeadCol)
        removeTail(canvas)

def snakePlaceFood(canvas):
    snakeBoard = canvas.data.snakeBoard
    (rows,cols) = (len(snakeBoard),len(snakeBoard[0]))
    (foodRow,foodCol) = (canvas.data.foodRow,canvas.data.foodCol)
    while True:
        foodRow = random.randint(0,rows-1)
        foodCol = random.randint(0,cols-1)
        if (snakeBoard[foodRow][foodCol] == 0):
            break
    snakeBoard[foodRow][foodCol] = -1
    (canvas.data.foodRow,canvas.data.foodCol) = (foodRow,foodCol)

def snakeGameOver(canvas):
    canvas.data.isSnakeGameOver = True

def snakePrintInstructions(canvas):
    # you write this!
    # print the instructions
    print """Snake!
    Use the arrow keys to move the snake.
    Eat food to grow.
    Stay on the board!
    And don't crash into yourself!
    Press 'd' for debug mode.
    Press 'r' to restart.
    Press 'q' to quit."""

def snakeInit(canvas):
    canvas.data.headRow = -1
    canvas.data.headCol = -1
    canvas.data.foodRow = -1
    canvas.data.foodCol = -1
    canvas.data.snakeDRow = 0
    canvas.data.snakeDCol = -1
    canvas.data.ignoreNextTimerEvent = False
    canvas.data.isSnakeGameOver = False
    canvas.data.inDebugMode = False
    snakePrintInstructions(canvas)
    loadSnakeBoard(canvas)
    snakeRedrawAll(canvas)

########### copy-paste below here ###########

def snakeRun(rows,cols):
    # create the root and the canvas
    root = Tk()
    margin = 5
    cellSize = 30
    canvasWidth = 2*margin + cols*cellSize
    canvasHeight = 2*margin + rows*cellSize
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.margin = margin
    canvas.data.cellSize = cellSize
    canvas.data.canvasRows = rows
    canvas.data.canvasCols = cols
    canvas.data.canvasWidth = canvasWidth
    canvas.data.canvasHeight = canvasHeight
    snakeInit(canvas)
    # set up events
    def f(event): snakeMousePressed(canvas, event)    
    root.bind("<Button-1>", f)
    def g(event): snakeKeyPressed(canvas, event)    
    root.bind("<Key>", g)
    snakeTimerFired(canvas)
    # and launch the app
    root.mainloop()
    # This call BLOCKS (so your program waits until you close the window!)

snakeRun(8,16)
