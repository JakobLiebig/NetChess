import random
import multiprocessing.connection 

import chess_core
import chess_game

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

class Session:
    def host(host, port):
        server = ChessServer(host, port)
        
        server.waitForClient()
        
        # assign colours
        playerColour = random.choice([chess_core.Piece.Colour.WHITE,
                                      chess_core.Piece.Colour.BLACK])
        opponentColour = chess_core.Piece.Colour.Opponent(playerColour)
        
        server.send(opponentColour)
        
        return Session(server, playerColour)
        
    def connect(host, port):
        # connect to session hoster
        client = ChessClient(host, port)
        
        playerColour = client.receive()
        
        return Session(client, playerColour)
    
    def __init__(self, connection, playerColour):
        self.__game = chess_game.Game()
        self.__connection = connection
        self.__playerColour = playerColour
    
    def getGame(self):
        return self.__game()
    
    def movePiece(self, move):
        self.__game.movePiece(move)
        
        self.__connection.send(move)
        
    def updateBoard(self):
        if self.__game.getActivePlayer() == self.__playerColour:
            move = self.__connection.receive()
        
            self.__game.movePiece(move)
    
    def cleanUp(self):
        self.__connection.close()