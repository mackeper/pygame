import sys, socket
from entity import Entity, Character
from chat import Chat
from PyQt4 import QtGui, QtCore

class Game(QtGui.QMainWindow):
   def __init__(self):
      self.width = 1280
      self.height = 720
      self.updateRate = 60
      self.timer = QtCore.QBasicTimer()
      super(Game, self).__init__()
      self.initUI()
      self.timer.start(1000/self.updateRate, self)

   def initUI(self):

      self.resize(self.width, self.height)
      self.setWindowTitle("Game")
      #self.center()

      self.frame = GameFrame(self, self.width, self. height)
      
      self.show()

   def center(self):
      screen = QtGui.QDesktopWidget().screenGeometry()
      size = self.geometry()
      self.move((screen.width()-size.width()/2),
                (screen.height()-size.height()/2))

   def timerEvent(self, event):
      if event.timerId() == self.timer.timerId():
         self.frame.update()
         self.frame.draw()
         
   def keyPressEvent(self, event):
      self.frame.keyPressEvent(event)

class GameFrame(QtGui.QFrame):

   def __init__(self, parent, width, height):
      super(GameFrame, self).__init__(parent)
      self.width = width
      self.height = height
      self.resize(self.width, self.height)

      #Chat
      self.chatMode = False
      self.chat = Chat(10,self.height - 210, 600, 200)

      #Entities
      self.entities = []
      #self.entities.append(Entity())

      #e = Entity()
      #e.setPos(200,200)
      #self.entities.append(e)
      
      self.character = Character()
      self.character.setPos(300,300)

      self.otherPlayers = []

      #Server connection
      self.offline = False
      self.sock = socket.socket()
      self.sock.connect(('127.0.0.1', 1338))
      self.updatesPerServerSync = 5
      self.serverSyncCounter = 0

   def closeEvent(self, event):
      print("closed window")
      
   def initFrame(self):
      self.isWaitingAfterLine = false

   def paintEvent(self, event):
      painter = QtGui.QPainter(self)
      color = QtGui.QColor(0x450045)
      
      for e in self.entities:
         e.draw(painter)

      for op in self.otherPlayers:
         op.draw(painter)
         
      self.character.draw(painter)
      self.chat.draw(painter)
      
   def draw(self):
      self.repaint()

   def update(self):
      self.character.update()
      self.serverSync()
      for e in self.entities:
         e.update()

      for op in self.otherPlayers:
         op.update()

      self.chat.update()

   def keyPressEvent(self, event):
      key = event.key()

      if self.chatMode and key == QtCore.Qt.Key_Return:
         self.character.newMessage(self.chat.getNewLine())
         self.chat.addNewMessage()
         self.chatMode = False
      
      if self.chatMode and key < 0x110000:
         self.chat.appendLetter(chr(key))
         return
      
      if key == QtCore.Qt.Key_W:
         self.character.moveUp()

      if key == QtCore.Qt.Key_S:
         self.character.moveDown()
         
      if key == QtCore.Qt.Key_A:
         self.character.moveLeft()
         
      if key == QtCore.Qt.Key_D:
         self.character.moveRight()

      if key == QtCore.Qt.Key_Y:
         self.chatMode = True


   def serverSync(self):
      if self.offline:
         return
      
      if self.serverSyncCounter != self.updatesPerServerSync:
         self.serverSyncCounter += 1
         return
      self.serverSyncCounter = 0
      
      #print("Send character")
      self.sock.send(b'\x00\x00\x00\x36')
      self.sock.send(b'\x00')
      byteChar = self.character.generateBytes()
      self.sock.send(len(byteChar).to_bytes(4, 'big'))
      self.sock.send(byteChar)

      #print("Get other characters")
      self.otherPlayers = []
      self.sock.send(b'\x00\x00\x00\x36')
      self.sock.send(b'\x01')
      while True:
         oneChar = self.readUndefinedLength()
         if oneChar == b'\x00':
            break
         newChar = Character()
         newChar.createFromBytes(oneChar)
         self.otherPlayers.append(newChar)
      #print('Got all chars')
      
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
   
def main():
   app = QtGui.QApplication([])
   game = Game()
   sys.exit(app.exec_())
   
if __name__ == '__main__':
   main()
