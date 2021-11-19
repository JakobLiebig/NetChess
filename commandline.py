import chess_core
import chess_session

class CommandlineInterface:
    def start(self):
        #print("Welcome to...")
        #CommandlineInterface.__displayBanner()
        
        self.__session = CommandlineInterface.__setupSessionDialog()
        
        self.__session.updateBoard()
        
        gameOver = False
        while not gameOver:
            curBoard = self.__session.getGame().getBoard()
            encodedBoard = CommandlineInterface.__encodeBoard(curBoard)
            
            CommandlineInterface.clearCommandLine()
            print(encodedBoard)
            
            move = CommandlineInterface.__getMoveDialog()
            
            self.__session.movePiece(move)
            self.__session.updateBoard()
        
        winner = self.__session.getGame().getActivePlayer()
        
        CommandlineInterface.__endDialog(winner)
        
    
    def clearCommandLine():
        print(chr(27) + "[2J")
    
    def __displayBanner():
        print(""" _______          __   _________ .__                         ._._.
 \      \   _____/  |_ \_   ___ \|  |__   ____   ______ _____| | |
 /   |   \_/ __ \   __\/    \  \/|  |  \_/ __ \ /  ___//  ___/ | |
/    |    \  ___/|  |  \     \___|   Y  \  ___/ \___ \ \___ \ \|\|
\____|__  /\___  >__|   \______  /___|  /\___  >____  >____  >____
        \/     \/              \/     \/     \/     \/     \/ \/\/""")
        
    def __setupSessionDialog():
        ...
    
    def __getMoveDialog():
        ...
    
    def __endDialog(winner):
        ...
    
    def __moveFromString(fromStr, toStr):
        fromX = ord(fromStr[0]) - ord("a")
        fromY = ord(fromStr[1]) - ord("1")
        from_ = fromX + fromY * 8
        
        toX = ord(toStr[0]) - ord("a")
        toY = ord(toStr[1]) - ord("1")
        to_ = toX + toY * 8
        
        return chess_core.Move(from_, to_)
    
    def __encodePiece(piece):
        if piece.getType() == chess_core.Piece.Type.KING:
            if piece.__colour == chess_core.Piece.Colour.WHITE:
                return "♚"
            else:
                return "♔"
        elif piece.getType() == chess_core.Piece.Type.QUEEN:
            if piece.__colour == chess_core.Piece.Colour.WHITE:
                return "♛"
            else:
                return "♕"
        elif piece.getType() == chess_core.Piece.Type.BISHOP:
            if piece.__colour == chess_core.Piece.Colour.WHITE:
                return "♝"
            else:
                return "♗"
        elif piece.getType() == chess_core.Piece.Type.KNIGHT:
            if piece.__colour == chess_core.Piece.Colour.WHITE:
                return "♞"
            else:
                return "♘"
        elif piece.getType() == chess_core.Piece.Type.ROOK:
            if piece.__colour == chess_core.Piece.Colour.WHITE:
                return "♜"
            else:
                return "♖"
        elif piece.getType() == chess_core.Piece.Type.PAWN:
            if piece.__colour == chess_core.Piece.Colour.WHITE:
                return "♟︎"
            else:
                return "♙"
        else:
            return "."
    
    def __encodeBoard(board) -> str:
        boardString = ""
        
        for y in range(8):
            for x in range(8):
                curIndex = x + y * 8
                
                curPiece = board.getPieceAt(curIndex)
                curPieceString = CommandlineInterface.__encodePiece(curPiece)
                
                boardString += curPieceString
            boardString += "\n"
        
        return boardString