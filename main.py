import sys, socket
from PyQt4 import QtGui, QtCore

from entity import Entity, Character
from chat import Chat
from message import Message
from world import World
from clientthread import ClientThread

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
         
   def keyReleaseEvent(self, event):
      self.frame.keyReleaseEvent(event)
      
   def keyPressEvent(self, event):
      self.frame.keyPressEvent(event)

class GameFrame(QtGui.QFrame):

   def __init__(self, parent, width, height):
      super(GameFrame, self).__init__(parent)
      self.width = width
      self.height = height
      self.resize(self.width, self.height)

      #Input
      self.keys = {}

      #Chat
      self.chatMode = False
      self.chat = Chat(10,self.height - 210, 600, 200)

      #World (holds map size, entities, characters/players)
      self.world = World()
      
      #Character
      character = Character()
      character.setName("Macke")
      character.setPos(300,300)
      self.world.setCharacter(character)
      
      #Server connection
      self.threadHandler = ClientThread(self.world.getCharacter(),
                                        self.world.getOtherPlayers())
      self.threadHandler.start()

   def closeEvent(self, event):
      print("closed window")
      
   def initFrame(self):
      self.isWaitingAfterLine = false

   def paintEvent(self, event):
      painter = QtGui.QPainter(self)
      color = QtGui.QColor(0x450045)
      
      for e in self.world.getEntities():
         e.draw(painter)

      for op in self.world.getOtherPlayers():
         op.draw(painter)
         
      self.world.getCharacter().draw(painter)

      self.chat.draw(painter)
      
   def draw(self):
      self.repaint()

   def update(self):

      for k,v in self.keys.items():
         self.handleKeys(k,v)
      
      self.world.getCharacter().update()
      
      self.world.setOtherPlayers(self.threadHandler.getOtherPlayers())
      for e in self.world.getEntities():
         e.update()
         
      for op in self.world.getOtherPlayers():
         op.update()

      self.chat.update()

   def handleKeys(self, key, value):
      
      if key == QtCore.Qt.Key_W and not value:
         self.world.getCharacter().stopUp()
         
      if key == QtCore.Qt.Key_S and not value:
         self.world.getCharacter().stopDown()
         
      if key == QtCore.Qt.Key_A and not value:
         self.world.getCharacter().stopLeft()
         
      if key == QtCore.Qt.Key_D and not value:
         self.world.getCharacter().stopRight()

      if key == QtCore.Qt.Key_W and value: 
         self.world.getCharacter().moveUp()

      if key == QtCore.Qt.Key_S and value:
         self.world.getCharacter().moveDown()
         
      if key == QtCore.Qt.Key_A and value:
         self.world.getCharacter().moveLeft()
         
      if key == QtCore.Qt.Key_D and value:
         self.world.getCharacter().moveRight()


   def keyReleaseEvent(self, event):
      key = event.key()
      self.keys[key] = False
      event.accept()
      
         
   def keyPressEvent(self, event):
      key = event.key()
      self.keys[key] = True
      event.accept()

      if self.chatMode and key == QtCore.Qt.Key_Return:
         m = Message(self.chat.getNewLine(), self.world.getCharacter().getName())
         self.world.getCharacter().newMessage(m)
         self.chat.addMessage(m)
         self.chatMode = False
         self.chat.clearNewLine()
      
      if self.chatMode and key < 0x110000:
         self.chat.appendLetter(chr(key))
         return

      if key == QtCore.Qt.Key_Y:
         self.chatMode = True
      

def main():
   app = QtGui.QApplication([])
   game = Game()
   sys.exit(app.exec_())
   
if __name__ == '__main__':
   main()
