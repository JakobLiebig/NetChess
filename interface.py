import random

import chess_core
import chess_networking

class Interface:
    def setup(self):
        command = input("0 to start, 1 to join a session:")
        if command == "0":
            port = input("Port:")
            host = "localhost" # ???
            
            self.__connection = chess_networking.ChessServer(host, int(port))
            
            self.__connection.waitForClient()
            
            # assign colours
            self.__playerColour = random.choice([chess_core.Piece.Colour.WHITE,
                                    chess_core.Piece.Colour.BLACK])
            opponentColour = chess_core.Piece.Colour.Opponent(self.__playerColour)
            self.__connection.send(opponentColour)
            
        elif command == "1":
            port = input("Port:")
            host = input("Host:")
            
            client = chess_networking.ChessClient(host, int(port))
            
            playerColour = client.receive()
            
            self.__connection = client
            self.__playerColour = playerColour
        
        self.__game = chess_core.Game()

    def getUserMove(self):
        moveStrArr = input("Your turn:").split(" ")
        move = chess_core.Move.fromString(moveStrArr[0], moveStrArr[1])

        return move

    def getOpponentMove(self):
        move = self.__connection.receive()
    
        return move

    def startGame(self):
        gameOver = False
        
        while not gameOver:
            boardStr = str(self.__game.getBoard())
            print(boardStr)
            
            if self.__game.getActivePlayer() == self.__playerColour:
                move = self.getUserMove()
                
                self.__connection.send(move)
            else:
                move = self.getOpponentMove()
            
            gameOver = self.__game.movePiece(move)
        
        winner = self.__game.getActivePlayer()
        return winner == self.__playerColour