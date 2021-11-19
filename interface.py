import random

import chess_core
import chess_networking

class Interface:
    def setupServer(self):
        port = input("Port:")
        host = input("Host:")
            
        try:
            self.__connection = chess_networking.ChessServer(host, int(port))
        except PermissionError:
            raise ValueError("Port not available!")
            
        self.__connection.waitForClient()
            
        # host determines colours
        self.__playerColour = random.choice([chess_core.Piece.Colour.WHITE,
                                                chess_core.Piece.Colour.BLACK])
        opponentColour = chess_core.Piece.Colour.Opponent(self.__playerColour)
            
        # sends pick to client
        self.__connection.send(opponentColour)
            
    
    def setupClient(self):
        port = input("Port:")
        host = input("Host:")
            
        try:
            client = chess_networking.ChessClient(host, int(port))
            
        except ConnectionRefusedError:
            raise ValueError(f"Failed to Connect to {host}:{port}.")
                
            # host determines colours
        playerColour = client.receive()
            
        self.__connection = client
        self.__playerColour = playerColour

    
    def setup(self):
        command = input("0 to start, 1 to join a session:")
        
        if command == "0":
            self.setupServer()
        elif command == "1":
            self.setupClient()        
        elif command == "exit":
            quit()
        
        else:
            raise ValueError("Entry has to be either 0 or 1!")
        
        self.__game = chess_core.Game()

    def cleanup(self):
        self.__connection.close()
        
    def getUserMove(self):
        while True:
            try:
                moveStrArr = input("Your turn:").split(" ")
        
                move = chess_core.Move.fromString(moveStrArr[0], moveStrArr[1])
                
                if not self.__game.isLegalMove(move):
                    print("Please enter a valid Move!")
                else:
                    break
            except:
                print("Failed to convert entry to move! Please try again!")
                
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