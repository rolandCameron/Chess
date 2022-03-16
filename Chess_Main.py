import numpy as np
import sys
import pygame

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

boardSize = 1000
numSq = 8
sqSize = boardSize/numSq

bSq = (204,	85, 13)
bSqDark = (164, 45, 0)
wSq = (240, 191, 96)
wSqDark = (200, 151, 56)
recentClick = [0, 0]

startFEN = "r2Bk2r/ppp2ppp/2p5/8/4n1b1/3P4/PPP1KbPP/RN1Q1B1R w kq - 2 9"

width, height = boardSize, boardSize
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
    "k": k,
    "Q": Q,
    "q": q,
    "B": B,
    "b": b,
    "N": N,
    "n": n,
    "R": R,
    "r": r,
    "P": P,
    "p": p,
    "-": _
}

#Board
board = np.array([[_ for x in range(numSq)] for y in range(numSq)])
darkenedSquares = np.array([[False for x in range(numSq)] for y in range(numSq)])

#Functions
def isInt(integer):
    try:
        integer = int(integer)
        return True
    except:
        return False

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
        lastClick = recentClick
        pos = pygame.mouse.get_pos()

        sqClicked = getSquareClicked(pos)

        if board[sqClicked[0], sqClicked[1]] != _:
            recentClick = sqClicked
            if recentClick == lastClick:
                darkenedSquares[recentClick[0], recentClick[1]] = False
            else:
                darkenedSquares[recentClick[0], recentClick[1]] = True
                darkenedSquares[lastClick[0], lastClick[1]] = False
        else:
            pass
  # Update.
  
  # Draw.
  
  pygame.display.flip()
  fpsClock.tick(fps)