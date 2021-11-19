from signal import signal, SIGPIPE, SIG_DFL  
signal(SIGPIPE,SIG_DFL)

import multiprocessing.connection 

class ChessClient:
    def __init__(self, host, port):
        self.__client = multiprocessing.connection.Client((host, port))

    def __del__(self):
        self.__client.close()
            
    def send(self, move):
        self.__client.send(move)
    
    def receive(self):
        move = self.__client.recv()
        
        return move

class ChessServer:
    def __init__(self, host, port):
        self.__listener = multiprocessing.connection.Listener((host, port))
        self.__connection = None

    def __del__(self):
        self.__connection.close()
        self.__listener.close()
    
    def waitForClient(self):
        self.__connection = self.__listener.accept()
    
    def send(self, move):
        self.__connection.send(move)
    
    def receive(self):
        move = self.__connection.recv()
        
        return move