from copy import copy, deepcopy

##chess program

B = 'black'
W = 'white'

p = 'pawn'
n = 'knight'
b = 'bishop'
r = 'rook'
q = 'queen'
k = 'king'

bp = (p,B)
bn = (n,B)
bb = (b,B)
br = (r,B)
bq = (q,B)
bk = (k,B)

wp = (p,W)
wn = (n,W)
wb = (b,W)
wr = (r,W)
wq = (q,W)
wk = (k,W)

initBoard = [[wr, wn, wb, wq, wk, wb, wn, wr],
             [wp, wp, wp, wp, wp, wp, wp, wp],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [bp, bp, bp, bp, bp, bp, bp, bp],
             [br, bn, bb, bq, bk, bb, bn, br]]

all_directions = {n: [(1,2,False),
                  (2,1,False),
                  (-1,2,False),
                  (-2,-1,False),
                  (-2,1,False),
                  (1,-2,False),
                  (2,-1,False),
                  (1,-2,False)],
              b: [(1,1,True),(1,-1,True),(-1,-1,True),(-1,1,True)],
              r: [(1,0,True),(0,1,True),(0,-1,True), (-1,0,True)],
              k: [(0,1,False),(1,1,False),(0,-1,False),(1,-1,False),
                  (-1,0,False),(-1,1,False),(-1,-1,False),(1,0,False)],
              q:[(0,1,True),(1,1,True),(0,-1,True),(1,-1,True),
                  (-1,0,True),(-1,1,True),(-1,-1,True),(1,0,True)],
              p:[(1,0,False)]}
#TODO: problem with pawn

def getSquare(board,square):
    y,x = square
    return board[y][x]

def getMoves(square, board):
    piece = getSquare(board,square)
    if piece == 0:
        return []
    kind, color = piece
    directions = all_directions[kind]
    return makeMoves(kind, directions, color, board, square)

def isEmpty(square, board):
    tmp = getSquare(board, square)
    return tmp == 0

def extractCoords(direction):
    return (direction[0], direction[1])

def addCoords(c1, c2):
    return (c1[0]+c2[0],c1[1]+c2[1])

def inBoard(square):
    y,x = square
    return y >= 0 and y <= 7 and x >= 0 and x <= 7

def takeOneDirection(initSquare,direction, color,board):
    extend = direction[2]
    direction_coords = extractCoords(direction)
    targetSquare = addCoords(initSquare,direction_coords)
    if not inBoard(targetSquare):
        return []
    targetContent = getSquare(board,targetSquare)
    if not extend:
        print targetContent
        if targetContent == 0 or targetContent[1] != color:
            return [targetSquare]
        else:
            return []
    else:
        res = []
        while inBoard(targetSquare) and isEmpty(targetSquare, board):
            res.append(targetSquare)
            targetSquare = addCoords(targetSquare,direction)
        if inBoard(targetSquare):
            targetContent = getSquare(board,targetSquare)
            if targetContent != 0:
                if targetContent[1] != color:
                    res.append(targetSquare)
        return res


def makeMoves(kind, directions, color, board, square):
    if kind == 'p':
        if isSecondRank(square,color):
            directions.append((2,0,False))
    res = []
    for direction in directions:
        res += takeOneDirection(square, direction, color, board)
    return res


def playMove(move,board):
    _from, _to = move
    piece = board[_from[0]][_from[1]]
        
    newBoard = deepcopy(board)
    newBoard[_from[0]][_from[1]] = 0
    newBoard[_to[0]][_to[1]] = piece
    return newBoard


def getPieces(color, board):
    """returns the list of squares containing a piece of color *color*."""
    res = []
    for y in range(8):
        for x in range(8):
           tmpSquare = (y,x)
           tmpPiece = board[y][x]
           if tmpPiece != 0 and tmpPiece[1] == color:
               res.append(tmpSquare)
    return res

def getKing(color, board):
    for y in range(8):
        for x in range(8):
           tmpSquare = (y,x)
           tmpPiece = board[y][x]
           if tmpPiece != 0  and tmpPiece[0] == k and tmpPiece[1] == color:
               return tmpSquare

def getOppositeColor(color):
    return W if color == B else B

def isCheck(board, color):
    oppositeColor = getOppositeColor(color)
    oppositePieces = getPieces(oppositeColor, board)
    kingSquare = getKing(color, board)
    for square in oppositePieces:
        #tmpPiece = getSquare(board, square)
        moves = getMoves(square, board)
        if kingSquare in moves:
            return True
    return False


def isCheckMate(board, color):
    if not isCheck(board, color):
        return False
    kingSquare = getKing(color, board)
    kingMoves = getMoves(kingSquare, board)
    for move in kingMoves:
        tmpBoard = playMove(move, board)
        if not isCheck(tmpBoard, color):
            return False
    squares = getPieces(color, board)
    #TODO: filter out moves that don't do anything
    for square in squares:
        piece = getSquare(board,square)
        if piece[0] == k:
            continue
        moves = getMoves(square, board)
        for move in moves:
            tmpBoard = playMove(move, board)
            if not isCheck(tmpBoard,color):
                return False
    return True
