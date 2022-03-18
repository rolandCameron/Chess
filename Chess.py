from tkinter import W
import numpy as np
import sys
import pygame

pygame.init()

monitorInfo = pygame.display.Info()

fps = 60
fpsClock = pygame.time.Clock()

boardSize = monitorInfo.current_h - 70
sidebar = 0
numSq = 8
sqSize = boardSize/numSq

bSq = (204,	85, 13)
bSqDark = (164, 45, 0)
wSq = (240, 191, 96)
wSqDark = (200, 151, 56)
recentClick = [3, 3]
selectedSq = "none"
global turn

startFEN = "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1" #FEN string the game is started on

width, height = boardSize + sidebar, boardSize
screen = pygame.display.set_mode((width, height))

#Import pieces
K = pygame.image.load("C:/Users/18296/.vscode/Chess/Chess_Pieces/K.png")
K = pygame.transform.scale(K, (sqSize, sqSize))
k = pygame.image.load("C:/Users/18296/.vscode/Chess/Chess_Pieces/_K.png")
k = pygame.transform.scale(k, (sqSize, sqSize))
Q = pygame.image.load("C:/Users/18296/.vscode/Chess/Chess_Pieces/Q.png")
Q = pygame.transform.scale(Q, (sqSize, sqSize))
q = pygame.image.load("C:/Users/18296/.vscode/Chess/Chess_Pieces/_Q.png")
q = pygame.transform.scale(q, (sqSize, sqSize))
B = pygame.image.load("C:/Users/18296/.vscode/Chess/Chess_Pieces/B.png")
B = pygame.transform.scale(B, (sqSize, sqSize))
b = pygame.image.load("C:/Users/18296/.vscode/Chess/Chess_Pieces/_B.png")
b = pygame.transform.scale(b, (sqSize, sqSize))
N = pygame.image.load("C:/Users/18296/.vscode/Chess/Chess_Pieces/N.png")
N = pygame.transform.scale(N, (sqSize, sqSize))
n = pygame.image.load("C:/Users/18296/.vscode/Chess/Chess_Pieces/_N.png")
n = pygame.transform.scale(n, (sqSize, sqSize))
R = pygame.image.load("C:/Users/18296/.vscode/Chess/Chess_Pieces/R.png")
R = pygame.transform.scale(R, (sqSize, sqSize))
r = pygame.image.load("C:/Users/18296/.vscode/Chess/Chess_Pieces/_R.png")
r = pygame.transform.scale(r, (sqSize, sqSize))
P = pygame.image.load("C:/Users/18296/.vscode/Chess/Chess_Pieces/P.png")
P = pygame.transform.scale(P, (sqSize, sqSize))
p = pygame.image.load("C:/Users/18296/.vscode/Chess/Chess_Pieces/_P.png")
p = pygame.transform.scale(p, (sqSize, sqSize))
_ = pygame.image.load("C:/Users/18296/.vscode/Chess/Chess_Pieces/-.png")
_ = pygame.transform.scale(_, (0, 0))

#Pieces Dict
pieces = {
    "K": K,
    K: "K",
    "k": k,
    k: "k",
    "Q": Q,
    Q: "Q",
    "q": q,
    q: "q",
    "B": B,
    B: "B",
    "b": b,
    b: "b",
    "N": N,
    N: "N",
    "n": n,
    n: "n",
    "R": R,
    R: "R",
    "r": r,
    r: "r",
    "P": P,
    P: "P",
    "p": p,
    p: "p",
    "-": _,
    _: "_"
}

#Turn flip dict
turnFlip = {
    "w": "b",
    "b": "w"
}

#Board
board = np.array([[_ for x in range(numSq)] for y in range(numSq)])
darkenedSquares = np.array([[False for x in range(numSq)] for y in range(numSq)])
hasMoved = np.array([[0 for x in range(numSq)] for y in range(numSq)])

#Functions
def isInt(integer):
    try:
        integer = int(integer)
        return True
    except:
        return False

def pcColour(pcCoords):
    if pieces[board[pcCoords[0], pcCoords[1]]] == "_":
        return turnFlip[turn]
    elif pieces[board[pcCoords[0], pcCoords[1]]] != pieces[board[pcCoords[0], pcCoords[1]]].lower():
        return "w"
    else:
        return "b"

def absChange(pcPos, desPos):
    absXChange = abs(pcPos[0] - desPos[0])
    absYChange = abs(pcPos[1] - desPos[1])
    absChange = [absXChange, absYChange]
    return absChange

def changeDir(pcPos, desPos):
    dirs = [0, 0]
    if pcPos[0] > desPos[0]:
        dirs[0] = -1
    else:
        dirs[0] = 1
    if pcPos[1] > desPos[1]:
        dirs[1] = -1
    else:
        dirs[1] = 1
    return dirs

def checkCardinal(pcPos, desPos):
    change = absChange(pcPos, desPos)
    dirs = changeDir(pcPos, desPos)
    if change[0] == 0:
        for i in range(change[1] - 1):
            if board[pcPos[0], (pcPos[1] + ((i+1)*dirs[1]))] != _:
                return False
        return True
    elif change[1] == 0:
        for i in range(change[0] - 1):
            if board[(pcPos[0] + ((i+1)*dirs[0])), pcPos[1]] != _:
                return False
        return True
    else:
        return False

def checkDiagonal(pcPos, desPos):
    change = absChange(pcPos, desPos)
    dirs = changeDir(pcPos, desPos)
    if change[0] == change[1]: 
        for i in range(change[0] - 1):
            if board[(pcPos[0] + (i + 1) * dirs[0]), (pcPos[1] + (i + 1) * dirs[1])] != _:
                return False
        return True
    else:
        return False

def checkLegal(pcPos, desPos):
    if pcColour(pcPos) == pcColour(desPos):
        return False
    
    if pieces[board[pcPos[0], pcPos[1]]].lower() == "n":
        change = absChange(pcPos, desPos)
        if change[0] == 2 and change[1] == 1:
            return True
        elif change[0] == 1 and change[1] == 2:
            return True
        else:
            return False

    elif pieces[board[pcPos[0], pcPos[1]]].lower() == "k":
        change = absChange(pcPos, desPos)
        if change[0] == 1 and change[1] == 1:
            return True
        elif change[0] == 1 and change[1] == 0:
            return True
        elif change[0] == 0 and change[1] == 1:
            return True
        else:
            return False
    
    elif pieces[board[pcPos[0], pcPos[1]]].lower() == "r":
        return checkCardinal(pcPos, desPos)
    
    elif pieces[board[pcPos[0], pcPos[1]]].lower() == "b":
        return checkDiagonal(pcPos, desPos)
    
    elif pieces[board[pcPos[0], pcPos[1]]].lower() == "q":
        if checkCardinal(pcPos, desPos):
            return True
        elif checkDiagonal(pcPos, desPos):
            return True
        else:
            return False
    
    elif pieces[board[pcPos[0], pcPos[1]]].lower() == "p":
        change = absChange(pcPos, desPos)
        if change[0] > 1 and hasMoved[pcPos[0], pcPos[1]] == "1":
            return False
        elif change[0] == 2 and hasMoved[pcPos[0], pcPos[1]] == "0":
            pass

    else:
        return True
    
def drawBoard():
    for x in range(numSq):
        for y in range(numSq):
            if (x + y) % 2 == 0:
                if darkenedSquares[x, y]:
                    pygame.draw.rect(screen, (wSqDark), (sqSize * x, sqSize * y, sqSize * (x+1), sqSize * (y+1)))
                else:
                    pygame.draw.rect(screen, (wSq), (sqSize * x, sqSize * y, sqSize * (x+1), sqSize * (y+1)))
            else:
                if darkenedSquares[x, y]:
                    pygame.draw.rect(screen, (bSqDark), (sqSize * x, sqSize * y, sqSize * (x+1), sqSize * (y+1)))
                else:
                    pygame.draw.rect(screen, (bSq), (sqSize * x, sqSize * y, sqSize * (x+1), sqSize * (y+1)))

def drawPieces():
    for x in range(numSq):
        for y in range(numSq):
            screen.blit(board[x, y], (sqSize * x, sqSize * y))

def getSquareClicked(pos):
    posX = pos[0]
    posY = pos[1]
    for x in range(numSq):
        lowerBoundX = sqSize * x
        upperBoundX = sqSize * (x+1)
        if posX > upperBoundX or posX < lowerBoundX:
            continue
        for y in range(numSq):
            lowerBoundY = sqSize * y
            upperBoundY = sqSize * (y+1)
            if posY < upperBoundY and posY > lowerBoundY:
                sq = [x ,y]
                return sq

def decodeFEN(FEN):
    global turn

    FENsplit = FEN.split()
    pcs = FENsplit[0]
    rows = pcs.split("/")
    for y in range(numSq):
        rowY = rows[y]
        skip = 0
        for x in range(len(rowY)):
            if not isInt(rowY[x]):
                board[x + skip, y] = pieces[rowY[x]]                
            elif int(rowY[x]) > 1:
                skip += (int(rowY[x]) - 1)
    
    if FENsplit[1] == "w":
        turn = "w"
    else:
        turn = "b"

decodeFEN(startFEN)

# Game loop.
while True:
  screen.fill((0, 0, 0))
  drawBoard()
  drawPieces()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()

        recentClick = getSquareClicked(pos)

        if selectedSq == "none":
            selectedSq = recentClick
            darkenedSquares[selectedSq[0], selectedSq[1]] = True
        elif recentClick == selectedSq:
            darkenedSquares[selectedSq[0], selectedSq[1]] = False
            selectedSq = "none"
    
    if event.type == pygame.MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos()

        recentClick = getSquareClicked(pos)

        if selectedSq != recentClick and selectedSq != "none":
            if pcColour(selectedSq) == turn:
                if board[selectedSq[0], selectedSq[1]] != _:
                    if checkLegal(selectedSq, recentClick):
                        if board[recentClick[0], recentClick[1]] != _:
                            board[recentClick[0], recentClick[1]] = board[selectedSq[0], selectedSq[1]]
                            if selectedSq != recentClick:
                                board[selectedSq[0], selectedSq[1]] = _
                        else:
                            board[recentClick[0], recentClick[1]] = board[selectedSq[0], selectedSq[1]]
                            board[selectedSq[0], selectedSq[1]] = _
                        hasMoved[selectedSq[0], selectedSq[1]] = 1
                        turn = turnFlip[turn]
                darkenedSquares[selectedSq[0], selectedSq[1]] = False
                selectedSq = "none"
  # Update.

  # Draw.

  pygame.display.flip()
  fpsClock.tick(fps) 