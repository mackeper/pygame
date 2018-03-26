import socket, threading, time
from entity import Entity, Character
from chat import Chat

TCP_ADDRESS = "127.0.0.1"
TCP_PORT = 1338

class ClientThread(threading.Thread):
    def __init__(self, character, otherPlayers):
        threading.Thread.__init__(self)
        self.character = character
        self.otherPlayers = otherPlayers
        self.open = True

        #Server connection
        self.sock = socket.socket()
        self.sock.connect((TCP_ADDRESS, TCP_PORT))
        self.updatesPerSecond = 64
        
    def sendAuth(self):
        self.sock.send(b'\x00\x00\x00\x36')
        
    def sendCharacter(self):
        #print("Send character")
        self.sendAuth()
        self.sock.send(b'\x00')
        byteChar = self.character.generateBytes()
        self.sock.send(len(byteChar).to_bytes(4, 'big'))
        self.sock.send(byteChar)

    def getCharacters(self):
        #print("Get other characters")
        self.sendAuth()
        newOtherPlayers = []
        self.sock.send(b'\x01')
        while True:
            oneChar = self.readUndefinedLength()
            if oneChar == b'\x00':
                break
            newChar = Character()
            newChar.createFromBytes(oneChar)
            newOtherPlayers.append(newChar)
        self.otherPlayers = newOtherPlayers

    def sendMessage(self, m):
        self.sendAuth()
        self.sock.send(b'\x02')
        
    
    def readData(self, length):
        data = b""
        leftToRead = length
        while(leftToRead > 0):
            d = self.sock.recv(min(2048, leftToRead))
            leftToRead = leftToRead - len(d)
            data += d
        return data

    def readUndefinedLength(self):
        length = int.from_bytes(self.readData(4), 'big')
        return self.readData(length)

    def getOtherPlayers(self):
        #print('get otherplayers')
        return self.otherPlayers
    
    def close(self):
        self.open = False

    def serverSync(self):
        self.sendCharacter()
        self.getCharacters()
        
    def run(self):
        while self.open:
            self.serverSync()
            time.sleep(1/self.updatesPerSecond)
        
