from enum import Enum
import copy
from typing import ValuesView
    
class Move:
    def __init__(self, fromIndex: int, toIndex: int):
        self.__from = fromIndex
        self.__to = toIndex
    
    def __eq__(self, other):
        return self.__from == other.__from and self.__to == other.__to
    
    
    def getFrom(self):
        return self.__from

    def getTo(self):
        return self.__to
    
    
    def leavesBoardBoundaries(self):
        return self.__from >= 64 or self.__from < 0 or self.__to >= 64 or self.__to < 0
            
    def isStraightSlide(self):
        if self.leavesBoardBoundaries():
            return False

        xDirection = self.__to % 8 - self.__from % 8
        yDirection = self.__to // 8 - self.__from // 8
        
        return xDirection == 0 or yDirection == 0

    def isDiagonalSlide(self):
        if self.leavesBoardBoundaries():
            return False

        xDirection = self.__to % 8 - self.__from % 8
        yDirection = self.__to // 8 - self.__from // 8
        
        return abs(xDirection) == abs(yDirection)
    
    def isCapture(self, board):
        if self.leavesBoardBoundaries():
            return False

        activePiece = board.getPieceAt(self.__from)
        capturedPiece = board.getPieceAt(self.__to)
        
        return capturedPiece.getColour() == Piece.Colour.Opponent(activePiece.getColour())
        
    def isQueensideCastling(self, board):
        direction = self.__to - self.__from
        activePiece = board.getPieceAt(self.__from)

        return activePiece.getType() == Piece.Type.KING and direction == -2
    
    def isKingsideCastling(self, board):
        direction = self.__to - self.__from
        activePiece = board.getPieceAt(self.__from)

        return activePiece.getType() == Piece.Type.KING and direction == 2
     
    def isEnpassant(self, board):
        absDirection = abs(self.__to - self.__from)
        activePiece = board.getPieceAt(self.__from)
        
        return activePiece.getType() == Piece.Type.PAWN and not self.isCapture(board) and (absDirection == 9 or absDirection == 7)
    
    def isPawnPromotion(self, board):
        targetRow = self.__to // 8
        activePiece = board.getPieceAt(self.__from)
        
        return activePiece.getType() == Piece.Type.PAWN and (targetRow == 0 or targetRow == 7)
    
    def isKnightMove(self):
        if self.leavesBoardBoundaries():
            return False
        
        xDistance = abs(self.__to % 8 - self.__from % 8)
        yDistance = abs(self.__to // 8 - self.__from // 8)
        
        if (xDistance == 2 and yDistance == 1) or (xDistance == 1 and yDistance == 2):
            return True
        
        return False

class Piece:
    class Colour(Enum):
        NONE = 0
        WHITE = 1
        BLACK = 2
        
        def Opponent(colour):
            if colour == Piece.Colour.WHITE:
                return Piece.Colour.BLACK
            else:
                return Piece.Colour.WHITE         
    
    class Type(Enum):
        EMPTY = 0
        KING = 2
        QUEEN = 1
        BISHOP = 3
        KNIGHT = 4
        ROOK = 5
        PAWN = 6
    
    def empty():
        return Piece(Piece.Type.EMPTY, Piece.Colour.NONE)
    
    def king(colour: Colour):
        return Piece(Piece.Type.KING, colour)
    
    def queen(colour: Colour):
        return Piece(Piece.Type.QUEEN, colour)
    
    def bishop(colour: Colour):
        return Piece(Piece.Type.BISHOP, colour)
    
    def knight(colour: Colour):
        return Piece(Piece.Type.KNIGHT, colour)
    
    def rook(colour: Colour):
        return Piece(Piece.Type.ROOK, colour)
    
    def pawn(colour: Colour):
        return Piece(Piece.Type.PAWN, colour)
    
    
    def __init__(self, type, colour):
        self.__type = type
        self.__colour = colour
        self.__stepsTaken = 0
    
    def __eq__(self, other: object):
        return self.__colour == other.__colour and other.__type == self.__type
    
                
    def incrementStepsTaken(self):
        self.__stepsTaken += 1
    
    def getColour(self):
        return self.__colour
    
    def getType(self):
        return self.__type
    
    def setType(self, newType: Type):
        self.__type = newType
    
    def getStepsTaken(self):
        return self.__stepsTaken
    
    
    def generatePseudoLegalMoves(self, startingField, pseudoLegalMoves, board):
        if self.__type == Piece.Type.KING:
            self.__generateKingMoves(startingField, pseudoLegalMoves, board)
        elif self.__type == Piece.Type.QUEEN:
            self.__generateQueenMoves(startingField, pseudoLegalMoves, board)
        elif self.__type == Piece.Type.BISHOP:
            self.__generateBishopMoves(startingField, pseudoLegalMoves, board)
        elif self.__type == Piece.Type.KNIGHT:
            self.__generateKnightMoves(startingField, pseudoLegalMoves, board)
        elif self.__type == Piece.Type.ROOK:
            self.__generateRookMoves(startingField, pseudoLegalMoves, board)
        elif self.__type == Piece.Type.PAWN:
            self.__generatePawnMoves(startingField, pseudoLegalMoves, board)
    
    def __continueGenerateingSlidingMoves(self, firstMove, pseudoLegalMoves, board):
        firstMoveDirection = firstMove.getTo() - firstMove.getFrom()
        firstMoveDistance = abs(firstMoveDirection)
        
        currentField = firstMove.getFrom()
        
        while True:
            currentField += firstMoveDirection
            currentMove = Move(firstMove.getFrom(), currentField)
            
            isStraightSlide = (firstMoveDistance == 1 or firstMoveDistance == 8) and currentMove.isStraightSlide()
            
            isDiagonalSlide = (firstMoveDistance != 1 and firstMoveDistance != 8) and currentMove.isDiagonalSlide()
            
            if not isStraightSlide and not isDiagonalSlide:
                return

            pieceOnTargetField = board.getPieceAt(currentMove.getTo())
            
            if pieceOnTargetField.getType() == Piece.Type.EMPTY:
                # no piece on current field
                pseudoLegalMoves.append(currentMove)
            
            elif pieceOnTargetField.getColour() == self.__colour:
                # piece belongs to current player
                return

            elif pieceOnTargetField.getColour() != Piece.Colour.NONE:
                pseudoLegalMoves.append(currentMove)
                return
    
    def __generateKingMoves(self, startingField, pseudoLegalMoves, board):
        moveDirections = [1, -1, 9, -9, 8, -8, 7, -7]
        numMoveDirections = len(moveDirections)
        
        for moveIndex in range(0, numMoveDirections):
            curMove = Move(startingField, startingField + moveDirections[moveIndex])
            
            if not curMove.isDiagonalSlide() and not curMove.isStraightSlide():
                continue
            
            pieceOnTargetField = board.getPieceAt(curMove.getTo())
            
            if pieceOnTargetField.getColour() != self.__colour:
                pseudoLegalMoves.append(curMove)
        
        if self.__stepsTaken == 0:
            kingsideCastling = Move(startingField, startingField + 2)
            moveToKingsideRook = Move(startingField, startingField + 3)
            
            if board.isCastlingPossible(moveToKingsideRook):
                pseudoLegalMoves.append(kingsideCastling)
            
            queensideCastling = Move(startingField, startingField - 2)
            moveToQueensideRook = Move(startingField, startingField - 4)
            
            if board.isCastlingPossible(moveToQueensideRook):
                pseudoLegalMoves.append(queensideCastling)

    def __generateQueenMoves(self, startingField, pseudoLegalMoves, board):
        moveDirections = [1, -1, 9, -9, 8, -8, 7, -7]
        numMoveDirections = len(moveDirections)
        
        for moveIndex in range(0, numMoveDirections):
            curMove = Move(startingField, startingField + moveDirections[moveIndex])
            
            self.__continueGenerateingSlidingMoves(curMove, pseudoLegalMoves, board)
    
    def __generateBishopMoves(self, startingField, pseudoLegalMoves, board):
        moveDirections = [9, -9, 7, -7]
        numMoveDirections = len(moveDirections)
        
        for moveIndex in range(0, numMoveDirections):
            curMove = Move(startingField, startingField + moveDirections[moveIndex])
                    
            self.__continueGenerateingSlidingMoves(curMove, pseudoLegalMoves, board)
    
    def __generateKnightMoves(self, startingField, pseudoLegalMoves, board):
        moveDirections = [6, -6, 10, -10, 15, -15, 17, -17]
        numMoveDirections = len(moveDirections)
        
        for moveIndex in range(0, numMoveDirections):
            curMove = Move(startingField, startingField + moveDirections[moveIndex])
            
            if not curMove.isKnightMove():
                continue
            
            pieceAtTargetField = board.getPieceAt(curMove.getTo())
            
            if pieceAtTargetField.getColour() != self.__colour:
                pseudoLegalMoves.append(curMove)
    
    def __generateRookMoves(self, startingField, pseudoLegalMoves, board):
        moveDirections = [-1, 1, 8, -8]
        numMoveDirections = len(moveDirections)
        
        for moveIndex in range(0, numMoveDirections):
            curMove = Move(startingField, startingField + moveDirections[moveIndex])
            
            self.__continueGenerateingSlidingMoves(curMove, pseudoLegalMoves, board)
    
    def __generatePawnMoves(self, startingField, pseudoLegalMoves, board):
        if self.__colour == board.playerTop:
            advancingDirection = 8
        else:
            advancingDirection = -8

        activePlayersOpponent = Piece.Colour.Opponent(self.__colour)
        
        if self.__colour == board.playerTop:
            opponentDoublePawnOppeningRow = 4
        else:
            opponentDoublePawnOppeningRow = 3
        
        startingFieldRow = startingField // 8
        
        # possible moves:
        advanceOne = Move(startingField, startingField + advancingDirection)
        doubleOppening = Move(startingField, startingField + 2 * advancingDirection)
        captureLeft = Move(startingField, startingField + advancingDirection - 1)
        captureRight = Move(startingField, startingField + advancingDirection + 1)
        leftEnpassant = captureLeft
        rightEnpassant = captureRight
        
        # advanceOne
        # cannot leave board due to pawn promotion
        pieceOneAhead = board.getPieceAt(advanceOne.getTo())
        if pieceOneAhead.getType() == Piece.Type.EMPTY:
            pseudoLegalMoves.append(advanceOne)
            
            # double oppening
            if self.__stepsTaken == 0:
                
                pieceTwoAhead = board.getPieceAt(doubleOppening.getTo())
                if pieceOneAhead.getType() == Piece.Type.EMPTY:
                    pseudoLegalMoves.append(doubleOppening)
        
        
        # capture right
        if captureRight.isDiagonalSlide():
            capturedPieceRight = board.getPieceAt(captureRight.getTo())
            
            if captureRight.isCapture(board):
                pseudoLegalMoves.append(captureRight)
            elif capturedPieceRight.getType() == Piece.Type.EMPTY:
                # enpassant right
                capturedPiece = board.getPieceAt(startingField + 1)
                
                if capturedPiece.getColour() == activePlayersOpponent and capturedPiece.__stepsTaken == 1 and startingFieldRow == opponentDoublePawnOppeningRow:
                    pseudoLegalMoves.append(rightEnpassant)
                    
        
        # capture left
        if captureLeft.isDiagonalSlide():
            capturedPieceLeft = board.getPieceAt(captureLeft.getTo())
            
            if captureLeft.isCapture(board):
                pseudoLegalMoves.append(captureLeft)
            elif capturedPieceLeft.getType() == Piece.Type.EMPTY:
                # enpassant Left
                capturedPiece = board.getPieceAt(startingField + 1)
                
                if capturedPiece.getColour() == activePlayersOpponent and capturedPiece.__stepsTaken == 1 and startingFieldRow == opponentDoublePawnOppeningRow:
                    pseudoLegalMoves.append(leftEnpassant)

class Board:
    playerTop = Piece.Colour.WHITE
    playerBottom = Piece.Colour.BLACK
    
    def basicSetup():
        boardPieces = [Piece.empty()] * 64
        
        # place top Pieces
        boardPieces[0] = Piece.rook(Board.playerTop)
        boardPieces[1] = Piece.knight(Board.playerTop)
        boardPieces[2] = Piece.bishop(Board.playerTop)
        boardPieces[3] = Piece.queen(Board.playerTop)
        boardPieces[4] = Piece.king(Board.playerTop)
        boardPieces[5] = Piece.bishop(Board.playerTop)
        boardPieces[6] = Piece.knight(Board.playerTop)
        boardPieces[7] = Piece.rook(Board.playerTop)

        boardPieces[8] = Piece.pawn(Board.playerTop)
        boardPieces[9] = Piece.pawn(Board.playerTop)
        boardPieces[10] = Piece.pawn(Board.playerTop)
        boardPieces[11] = Piece.pawn(Board.playerTop)
        boardPieces[12] = Piece.pawn(Board.playerTop)
        boardPieces[13] = Piece.pawn(Board.playerTop)
        boardPieces[14] = Piece.pawn(Board.playerTop)
        boardPieces[15] = Piece.pawn(Board.playerTop)

        # place black Pieces
        boardPieces[63 - 0] = Piece.rook(Board.playerBottom)
        boardPieces[63 - 1] = Piece.knight(Board.playerBottom)
        boardPieces[63 - 2] = Piece.bishop(Board.playerBottom)
        boardPieces[63 - 3] = Piece.king(Board.playerBottom)
        boardPieces[63 - 4] = Piece.queen(Board.playerBottom)
        boardPieces[63 - 5] = Piece.bishop(Board.playerBottom)
        boardPieces[63 - 6] = Piece.knight(Board.playerBottom)
        boardPieces[63 - 7] = Piece.rook(Board.playerBottom)

        boardPieces[63 - 8] = Piece.pawn(Board.playerBottom)
        boardPieces[63 - 9] = Piece.pawn(Board.playerBottom)
        boardPieces[63 - 10] = Piece.pawn(Board.playerBottom)
        boardPieces[63 - 11] = Piece.pawn(Board.playerBottom)
        boardPieces[63 - 12] = Piece.pawn(Board.playerBottom)
        boardPieces[63 - 13] = Piece.pawn(Board.playerBottom)
        boardPieces[63 - 14] = Piece.pawn(Board.playerBottom)
        boardPieces[63 - 15] = Piece.pawn(Board.playerBottom)
        
        return Board(boardPieces)
    
    
    def __init__(self, boardPieces):
        self.__boardPieces = boardPieces
    
    
    def getPieceAt(self, index):
        return self.__boardPieces[index]
    
                
    def movePiece(self, move):
        nextStateBoardPieces = copy.deepcopy(self.__boardPieces)
        
        activePiece = nextStateBoardPieces[move.getFrom()]
        capturedPiece = nextStateBoardPieces[move.getTo()]
        
        if move.isQueensideCastling(self):
            rookPosition = move.getFrom() - 4
            rookTargetPosition = move.getFrom() - 1
            rook = nextStateBoardPieces[rookPosition]
            
            nextStateBoardPieces[rookTargetPosition] = rook
            nextStateBoardPieces[rookPosition] = Piece.empty()
            
            rook.incrementStepsTaken()
        
        elif move.isKingsideCastling(self):
            rookPosition = move.getFrom() + 3
            rookTargetPosition = move.getFrom() + 1
            rook = nextStateBoardPieces[rookPosition]
            
            nextStateBoardPieces[rookTargetPosition] = rook
            nextStateBoardPieces[rookPosition] = Piece.empty()
            
            rook.incrementStepsTaken()
        
        elif move.isEnpassant(self):
            capturedPawnPosition = move.getFrom() + (move.getTo() % 8) - (move.getFrom() % 8)
            
            nextStateBoardPieces[capturedPawnPosition] = Piece.empty()
        
        elif move.isPawnPromotion(self):
            activePiece.setType(Piece.Type.QUEEN)
        
        activePiece.incrementStepsTaken()
        nextStateBoardPieces[move.getTo()] = activePiece
        nextStateBoardPieces[move.getFrom()] = Piece.empty()
        
        return Board(nextStateBoardPieces)
    
        
    def generateLegalMoves(self, activePlayer):
        pseudoLegalMoves = self.__generatePseudoLegalMoves(self.__activePlayer)
        legalMoves = []
        
        for pseudoLegalMove in pseudoLegalMoves:
            nextState = self.movePiece(pseudoLegalMove)
            nextStatePseudoLegalMoves = nextState.__generatePseudoLegalMoves(self.__activePlayer)
            
            if not nextState.isKingUnderAttack(self.__activePlayer, nextStatePseudoLegalMoves):
                legalMoves.append(pseudoLegalMove)
        
        return legalMoves

    def __generatePseudoLegalMoves(self, activePlayer):
        pseudoLegalMoves = []
        
        for pieceIndex in range(64):
            Piece = self.__boardPieces[pieceIndex]
            
            if Piece.getColour() == activePlayer:
                Piece.generatePseudoLegalMoves(pieceIndex, pseudoLegalMoves, self)
        
        return pseudoLegalMoves
    
    
    def isCastlingPossible(self, moveToRook):
        rook = self.getPieceAt(moveToRook.getTo())
        isCastlingPossible = rook.getType() == Piece.Type.ROOK and rook.getStepsTaken() == 0
        
        directionToRook = moveToRook.getTo() - moveToRook.getFrom()
        
        if directionToRook >= 0:
            singleStepTowardsRook = 1
        else:
            singleStepTowardsRook = -1
        
        for i in range(moveToRook.getFrom() + singleStepTowardsRook, moveToRook.getTo()):
            isCastlingPossible = self.__boardPieces[i].getType() == Piece.Type.EMPTY
            
            if not isCastlingPossible:
                break
        
        return isCastlingPossible

    def isKingUnderAttack(self, kingOwner, pseudoLegalMovesOpponent):
        for move in pseudoLegalMovesOpponent:
            if self.__boardPieces[move.getTo()] == Piece.king(kingOwner):
                return True
        
        return False