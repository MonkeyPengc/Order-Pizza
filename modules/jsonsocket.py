
import json
import struct
import socket
import logging


class JsonSocket(object):
    """
    A base class for socket connection between client-server.
    Objects transmission with Json dependency.
    """
    
    def __init__(self, hostname='127.0.0.1', port=1617):
        self.__host = hostname
        self.__port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = self.socket
        logging.basicConfig()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
    
    def sendPackage(self, package):
        """
        Sender convert python objects to c structs. Packed
        as a python string according to given formats, and
        send to the receiver. (Python3 string-bytes)
        """
        
        msg = json.dumps(package)
        
        if self.socket:
            frmt = "={}s".format(len(msg))
            packedMsg = struct.pack(frmt, msg.encode('utf-8'))
            packedHdr = struct.pack('!I', len(packedMsg))
            
            self.send(packedHdr)
            self.send(packedMsg)

    def send(self, msg):
        sent = 0
        
        while sent < len(msg):
            sent += self.conn.send(msg[sent:])
                
    def readPackage(self):
        """ 
        Receiver read format strings of a certain size,
        unpack the string according to given format, and
        convert to python objects.
        """
        
        size = self.msgLength()
        data = self.read(size)
        frmt = "={}s".format(size)
        msg = struct.unpack(frmt, data)
        
        return json.loads(msg[0].decode('utf-8'))
    
    def read(self, size):
        data = b""
        
        while len(data) < size:
            dataTmp = self.conn.recv(size-len(data))
            data += dataTmp
            
            if dataTmp == '':
                self.logger.error("Socket connection broken.")
                raise RuntimeError
    
        return data

    def msgLength(self):
        """
        Get the size of format strings represented as a tuple
        """
        
        d = self.read(4)
        s = struct.unpack('!I', d)
        return s[0]

    def close(self):
        self.closeSocket()
        if self.socket is not self.conn:
            self.closeConnection()

    def closeSocket(self):
        self.logger.debug("Closing main socket.")
        self.socket.close()
    
    def closeConnection(self):
        self.logger.debug("Closing the connection socket.")
        self.conn.close()
    
    def get_host(self):
        return self.__host
    
    def set_host(self, host):
        pass
    
    def get_port(self):
        return self.__port
    
    def set_port(self, port):
        pass
    
    host = property(get_host, set_host,doc='read only property socket hostname.')
    port = property(get_port, set_port,doc='read only property socket port.')









