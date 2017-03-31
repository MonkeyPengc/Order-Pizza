
from .jsonsocket import JsonSocket
import threading
import time

class JsonServer(JsonSocket):
    """
    Inherit Json Socket class and enable standard server operations.
    Display current connected clients and time.
    """
    
    def __init__(self, hostname, port):
        super(JsonServer, self).__init__(hostname, port)
        self.bind()
        self.listen()
    
    def bind(self):
        self.socket.bind((self.get_host(), self.get_port()))
        print('Server established at', self.get_host(), self.get_port())
    
    def listen(self):
        self.socket.listen(5)
    
    def acceptConnection(self):
        self.conn, clientaddr = self.socket.accept()

    def now(self):
        return time.asctime()


class ThreadedServer(threading.Thread, JsonServer):
    """
    Inherit both JsonServer and python threading class,
    invoke threads to listen to clients, read package
    from clients, and process the package.
    Abstract method:
    Need a concrete implementation of processing package.
    """
    
    def __init__(self, hostname, port):
        threading.Thread.__init__(self)
        JsonServer.__init__(self, hostname, port)
        self.stopped = True
    
    def processPackage(self, package):
        raise NotImplementedError
    
    def run(self):
        self.stopped = not self.stopped
        
        while not self.stopped:
            self.acceptConnection()
            
            try:
                package = self.readPackage()
                self.processPackage(package)
            
            except Exception as e:
                print(e)
                self.closeConnection()
                break

        self.close()

    def stop(self):
        self.stopped = not self.stopped




