import random
import multiprocessing.connection 

import chess.core as core
import chess.game as game

class Session:
    class ChessClient:
        def __init__(self, host, port):
            self.__client = multiprocessing.connection.Client((host, port))
                
        def send(self, move):
            self.__client.send(move)
        
        def receive(self):
            move = self.__client.recv()
            
            return move

        def close(self):
            self.__client.close()

    class ChessServer:
        def __init__(self, host, port):
            self.__listener = multiprocessing.connection.Listener((host, port))
            self.__connection = None

        def waitForClient(self):
            self.__connection = self.__listener.accept()
        
        def send(self, move):
            self.__connection.send(move)
        
        def receive(self):
            move = self.__connection.recv()
            
            return move
        
        def close(self):
            self.__connection.close()
            self.__listener.close()

    
    def host(host, port):
        server = Session.ChessServer(host, port)
        
        server.waitForClient()
        
        # assign colours
        playerColour = random.choice([core.Piece.Colour.WHITE,
                                      core.Piece.Colour.BLACK])
        opponentColour = core.Piece.Colour.Opponent(playerColour)
        
        server.send(opponentColour)
        
        return Session(server, playerColour)
        
    def connect(host, port):
        client = Session.ChessClient(host, port)
        
        playerColour = client.receive()
        
        return Session(client, playerColour)
    
    def __init__(self, connection, playerColour):
        self.__game = game.Game()
        self.__connection = connection
        self.__playerColour = playerColour
    
    def getGame(self):
        return self.__game
    
    def getMyColour(self):
        return self.__playerColour
    
    def myTurn(self):
        return self.__game.getActivePlayer() == self.__playerColour
    
    def movePiece(self, move):
        gameOver = self.__game.movePiece(move)
        
        self.__connection.send(move)
        
        return gameOver
        
    def opponentMovePiece(self):
        move = self.__connection.receive()
        
        gameOver = self.__game.movePiece(move)
        
        return gameOver
    
    def cleanUp(self):
        self.__connection.close()