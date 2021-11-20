import time
from typing import Text

import chess.core as chess_core
import chess.session as chess_session

class CommandlineInterface:
    class TextColour:
        PURPLE = '\033[95m'
        CYAN = '\033[96m'
        DARKCYAN = '\033[36m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'
            
    def start(self):
        print("Welcome to...")
        CommandlineInterface.__displayBanner()
        
        self.__session = CommandlineInterface.__setupSessionDialog()

        print(CommandlineInterface.TextColour.GREEN, "\nConnected!", CommandlineInterface.TextColour.END)
        print(CommandlineInterface.TextColour.BOLD, f"You play {self.__encodeMyColour()}!", CommandlineInterface.TextColour.END)
        print(CommandlineInterface.TextColour.BOLD, "Please Enter Moves like this: <from> <to> (e.g. 'a2 c4')", CommandlineInterface.TextColour.END)      
        print("Game starts in 10 seconds!")
        time.sleep(10)
        
        try:
            winner = self.__gameLoop()
        
            self.__endDialog(winner)
        
        except Exception as ex:
                print(CommandlineInterface.TextColour.RED, "Terminated Game! Error: ", str(ex), CommandlineInterface.TextColour.END)
        finally:
            self.__session.cleanUp()
            
    def __setupHostDialog():
        while True:
            try:
                host = input("Select a host (e.g. localhost)>")
                port = int(input("Select a port (e.g. 1234)>"))
                
                print("Waiting for Opponent...")
                return chess_session.Session.host(host, port)
            except Exception as ex:
                print(CommandlineInterface.TextColour.RED, "Error! ", str(ex), CommandlineInterface.TextColour.END)
    
    def __setupClientDialog():
        while True:
            try:
                host = input("Host>")
                port = int(input("Port>"))
                
                print(f"Connecting to {host}:{port}...")
                return chess_session.Session.connect(host, port)
            except Exception as ex:
                print(CommandlineInterface.TextColour.RED, "Error! ", str(ex), CommandlineInterface.TextColour.END)
    
    def __setupSessionDialog():
        while True:
            try:
                print("Please type 0 to host a session or 1 to join one!")
                command = input(">")
                
                if command == "0":
                    return CommandlineInterface.__setupHostDialog()
                elif command == "1":
                    return CommandlineInterface.__setupClientDialog()
                else:
                    raise ValueError("Input has to be either 0 or 1!")
            except Exception as ex:
                print(CommandlineInterface.TextColour.RED, "Error! ", str(ex), CommandlineInterface.TextColour.END)
    
    def __getMoveDialog(self):
        while True:
            try:
                print("Your turn!")
                moveStr = input(">")
                moveStrAr = moveStr.split(" ")
                
                move = CommandlineInterface.__moveFromString(moveStrAr[0], moveStrAr[1])

                if not self.__session.getGame().isLegalMove(move):
                    raise ValueError("Not a legal Move!")
                
                return move
            except Exception as ex:
                print(CommandlineInterface.TextColour.RED, "Error! ", str(ex), CommandlineInterface.TextColour.END)
            
    def __endDialog(self, winner):
        if winner == self.__session.getMyColour():
            print(CommandlineInterface.TextColour.GREEN, "Game over! You win!", CommandlineInterface.TextColour.END)
        else:
            print(CommandlineInterface.TextColour.RED, "Game over! You loose!", CommandlineInterface.TextColour.END)
    
    
    def __moveFromString(fromStr, toStr):
        fromX = ord(fromStr[0]) - ord("a")
        fromY = ord(fromStr[1]) - ord("1")
        from_ = fromX + fromY * 8
        
        toX = ord(toStr[0]) - ord("a")
        toY = ord(toStr[1]) - ord("1")
        to_ = toX + toY * 8
        
        return chess_core.Move(from_, to_)
    
    def __encodePiece(piece):
        if piece.getType() ==chess_core.Piece.Type.KING:
            if piece.getColour() ==chess_core.Piece.Colour.WHITE:
                return "♚"
            else:
                return "♔"
        elif piece.getType() ==chess_core.Piece.Type.QUEEN:
            if piece.getColour() ==chess_core.Piece.Colour.WHITE:
                return "♛"
            else:
                return "♕"
        elif piece.getType() ==chess_core.Piece.Type.BISHOP:
            if piece.getColour() ==chess_core.Piece.Colour.WHITE:
                return "♝"
            else:
                return "♗"
        elif piece.getType() ==chess_core.Piece.Type.KNIGHT:
            if piece.getColour() ==chess_core.Piece.Colour.WHITE:
                return "♞"
            else:
                return "♘"
        elif piece.getType() ==chess_core.Piece.Type.ROOK:
            if piece.getColour() ==chess_core.Piece.Colour.WHITE:
                return "♜"
            else:
                return "♖"
        elif piece.getType() ==chess_core.Piece.Type.PAWN:
            if piece.getColour() ==chess_core.Piece.Colour.WHITE:
                return "♟︎"
            else:
                return "♙"
        else:
            return "."
    
    def __encodeBoard(board) -> str:
        boardString = "abcdefgh\n"
        
        for y in range(8):
            for x in range(8):
                curIndex = x + y * 8
                
                curPiece = board.getPieceAt(curIndex)
                curPieceString = CommandlineInterface.__encodePiece(curPiece)
                
                boardString += curPieceString
            boardString += f"{y+1}\n"
        
        return boardString

    def __displayBoard(self):
        curBoard = self.__session.getGame().getBoard()
        encodedBoard = CommandlineInterface.__encodeBoard(curBoard)
            
        CommandlineInterface.__clearCommandLine()
        print(encodedBoard)

    def __clearCommandLine():
        print(chr(27) + "[2J")
    
    def __displayBanner():
        print(CommandlineInterface.TextColour.PURPLE, """ _______          __   _________ .__                         ._._.
 \      \   _____/  |_ \_   ___ \|  |__   ____   ______ _____| | |
 /   |   \_/ __ \   __\/    \  \/|  |  \_/ __ \ /  ___//  ___/ | |
/    |    \  ___/|  |  \     \___|   Y  \  ___/ \___ \ \___ \ \|\|
\____|__  /\___  >__|   \______  /___|  /\___  >____  >____  >____
        \/     \/              \/     \/     \/     \/     \/ \/\/""", CommandlineInterface.TextColour.END)

    def __encodeMyColour(self):
        myColour = self.__session.getMyColour()
        if myColour == chess_core.Piece.Colour.WHITE:
            return "white"
        else:
            return "black"
            

    def __gameLoop(self):
        gameOver = False
        while not gameOver:
            self.__displayBoard()
            
            if self.__session.myTurn():
                move = self.__getMoveDialog()
                
                gameOver = self.__session.movePiece(move)
            else:
                print("Waiting for opponent move...")
                gameOver = self.__session.opponentMovePiece()
        
        winner = self.__session.getGame().getActivePlayer()
        return winner