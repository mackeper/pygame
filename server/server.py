import socket
import threading
from servermodel import ServerModel

TCP_ADDRESS = "127.0.0.1"
TCP_PORT = 27114

class Server():
    def __init__(self, address, port):
        self.currentId = 0
        self.address = address
        self.port = port
        self.idCounter = 0
        self.serverModel = ServerModel()

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.address, self.port))
        s.listen(0)
        print("Server started")
        while True:
            connection, address = s.accept()
            threadHandler = ServerThread(connection, address, self.idCounter, self.serverModel)
            print("New connection with id: " + str(self.idCounter))
            self.idCounter += 1
            threadHandler.start()
            
        s.close()

class ServerThread(threading.Thread):
    def __init__(self, connection, address, id, serverModel):
        threading.Thread.__init__(self)
        self.connection = connection
        self.address = address
        self.id = id
        self.serverModel = serverModel
        self.open = True
        
    def run(self):
        while self.open:
            try:
                self.recieve()
            except:
                print('disconnect: ' + str(self.id))
                break
            
        self.connection.close()
        
    def recieve(self):
        auth = int.from_bytes(self.readData(4), 'big')
        if auth != 54:
            return
        
        type = self.readData(1)
        if(type == b'\x00'):
            print("Character to server")
            self.serverModel.addCharacter(self.id, self.readUndefinedLength())
        elif(type == b'\x01'):
            print("Characters to client")
            self.sendCharacters()
        elif(type == b'\x02'):
            print("Message to server")
        elif(type == b'\x03'):
            print("Messages to client")
        elif(type == b'\x04'):
            print("Enitiy to server")
        elif(type == b'\x05'):
            print("Entities to client")

    def readData(self, length):
        data = b""
        leftToRead = length
        while(leftToRead > 0):
            d = self.connection.recv(min(2048, leftToRead))
            leftToRead = leftToRead - len(d)
            data += d
        return data

    def readUndefinedLength(self):
        length = int.from_bytes(self.readData(4), 'big')
        return self.readData(length)

    def sendCharacters(self):
        for k, v in self.serverModel.getCharacters().items():
            if k != self.id:
                self.connection.send(len(v).to_bytes(4, 'big'))
                self.connection.send(v)
        self.connection.send(b'\x00\x00\x00\x01')
        self.connection.send(b'\x00')
    
def main():
    server = Server('127.0.0.1', 1338)
    server.start()

if __name__ == '__main__':
    main()
