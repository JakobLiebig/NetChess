import chess_core

class Game:
    def __init__(self):
        self.__activePlayer = chess_core.Piece.Colour.WHITE
        self.__board = chess_core.Board.basicSetup()
        self.__currentStateLegalMoves = self.__board.generatePseudoLegalMoves(self.__activePlayer)
    
    def movePiece(self, move):
        if not self.isLegalMove(move):
            raise ValueError("Not a legal Move!")
        
        self.__board = self.__board.movePiece(move)
        
        self.__activePlayer = chess_core.Piece.Colour.Opponent(self.__activePlayer)
        
        self.__currentStateLegalMoves = self.__board.generateLegalMoves(self.__activePlayer)
        
        if len(self.__currentStateLegalMoves) == 0:
            return True
        else:
            return False
    
    def isLegalMove(self, move):
        return move in self.__currentStateLegalMoves
    
    def reset(self):
        self.__activePlayer = chess_core.Piece.Colour.WHITE
        self.__board = chess_core.Board.basicSetup()
    
    def getBoard(self):
        return self.__board
    
    def getActivePlayer(self):
        return self.__activePlayer
    
    def getLegalMoves(self):
        return self.__currentStateLegalMoves