from PyQt4 import QtGui, QtCore
import math

from message import Message

class Entity():
   def __init__(self):
      self.width = 20
      self.height = 20
      self.x = 100
      self.y = 100
      self.color = QtGui.QColor(69,0,69)
      self.blocking = True

      #Moving
      self.moving = {'up' : False, 'down' : False, 'right' : False, 'left' : False}
      self.moveTime = {'up' : 0, 'down' : 0, 'right' : 0, 'left' : 0}
      self.speedEpsilon = 0.01
      self.maxSpeed = 5
      self.acceleration = 0.2
      self.speedy, self.speedx = 0, 0
      
   def moveUp(self):
      self.moving['up'] = True
      
   def moveDown(self):
      self.moving['down'] = True

   def moveLeft(self):
      self.moving['left'] = True

   def moveRight(self):
      self.moving['right'] = True

   def stopMove(self, dir):
      if self.moving[dir] == True:
         self.moving[dir] = False

   def stopUp(self):
      self.stopMove('up')
      
   def stopDown(self):
      self.stopMove('down')

   def stopLeft(self):
      self.stopMove('left')

   def stopRight(self):
      self.stopMove('right')

   def addForce(self, x,y):
      self.speedx += x
      self.speedy += y
      
   def handleMovement(self, direction):

      if self.moving['right']:
         if self.speedx < self.maxSpeed:
            self.addForce(self.acceleration, 0)

      if self.moving['left']:
         if self.speedx > -self.maxSpeed:
            self.addForce(-self.acceleration, 0)
            
      if not self.moving['right'] and not self.moving['left']:
         self.speedx *= 0.9
         if abs(self.speedx) < self.speedEpsilon:
            self.speedx = 0

      if self.moving['up']:
         if self.speedy > -self.maxSpeed:
            self.addForce(0, -self.acceleration)

      if self.moving['down']:
         if self.speedy < self.maxSpeed:
            self.addForce(0, self.acceleration)
            
      if not self.moving['up'] and not self.moving['down']:
         self.speedy *= 0.9
         if abs(self.speedy) < self.speedEpsilon:
            self.speedy = 0

      self.x += self.speedx
      self.y += self.speedy
      
   def move(self):
      #for k,v in self.moving.items():
      self.handleMovement('')
      
   def update(self):
      self.move()
          
   def setPos(self, x, y):
      self.x, self.y = x, y

   def getPos(self):
      return (self.x, self.y)
   
   def draw(self, painter):
      painter.fillRect(self.x, self.y, self.width, self.height, self.color)

   def getColor(self):
      return self.color

   def setColor(self, r, g, b):
      self.color = QtGui.QColor(r,g,b)

class Character(Entity):
    def __init__(self):
       super().__init__()
       self.message = None
       self.color = QtGui.QColor(244,242,66)
       self.name = 'Unnamed'

    def newMessage(self, m):
       self.message = m
       
    def update(self):
       super().update()
       if self.message is not None:
           self.message.update()
           if self.message.isDead():
               self.message = None
               
    def draw(self, painter):
       painter.fillRect(self.x ,self.y, self.width, self.height, self.color)
       if self.message is not None:
           self.message.draw(painter, self.x, self.y)


    def generateBytes(self):
       """
       PROTOCOL
       * 4 bytes: name size
       * - bytes: name
       * 4 bytes: X coord
       * 4 bytes: Y coord
       * 4 bytes: X speed
       * 4 bytes: Y speed
       * 1 bytes: X speed negative = 1 else 0
       * 1 bytes: Y speed negative = 1 else 0
       * 1 byte: color red
       * 1 byte: color green
       * 1 byte: color blue
       * 1 byte: color alpha
       * 1 byte: Message exists 1 or 0
       * 4 bytes: message size
       * - bytes: message
       * 4 bytes: message time
       """
       #name
       bytes = b''
       bytes += len(self.name).to_bytes(4, 'big')
       bytes += self.name.encode()

       #position
       bytes += int(self.x).to_bytes(4, 'big')
       bytes += int(self.y).to_bytes(4, 'big')

       #speed
       bytes += int(abs(self.speedx)).to_bytes(4, 'big')
       if self.speedx < 0:
          bytes += b'\x01'
       else:
          bytes += b'\x00'
       bytes += int(abs(self.speedy)).to_bytes(4, 'big')
       if self.speedy < 0:
          bytes += b'\x01'
       else:
          bytes += b'\x00'

       #color
       bytes += self.color.red().to_bytes(1, 'big')
       bytes += self.color.green().to_bytes(1, 'big')
       bytes += self.color.blue().to_bytes(1, 'big')
       bytes += self.color.alpha().to_bytes(1, 'big')
       
       #message:
       if self.message != None:
          bytes += b'\x01'
          bytes += len(self.message.getString()).to_bytes(4, 'big')
          bytes += self.message.getString().encode()
          bytes += int(self.message.getTimeLeft()).to_bytes(4, 'big')
       else:
          bytes += b'\x00'
       return bytes

    def createFromBytes(self, byteChar):
       #Name:
       index = 0
       nameSize = int.from_bytes(byteChar[index:index+4], 'big')
       index += 4
       self.name = byteChar[index:index+nameSize].decode()
       index += nameSize
       #Position
       self.x = int.from_bytes(byteChar[index:index+4], 'big')
       index += 4
       self.y = int.from_bytes(byteChar[index:index+4], 'big')
       index += 4
       #Speed
       self.speedx = int.from_bytes(byteChar[index:index+4], 'big')
       index += 4
       if byteChar[index] == 1:
          self.speedx *= -1
       index += 1
       self.speedy = int.from_bytes(byteChar[index:index+4], 'big')
       index += 4
       if byteChar[index] == 1:
          self.speedy *= -1
       index += 1

       #Color:
       self.color.setRed(byteChar[index])
       index += 1
       self.color.setGreen(byteChar[index])
       index += 1
       self.color.setBlue(byteChar[index])
       index += 1
       self.color.setAlpha(byteChar[index])
       index += 1
       
       #Message:
       if byteChar[index] == 1:
          index += 1
          messageSize = int.from_bytes(byteChar[index:index+4], 'big')
          index += 4
          self.message = Message(byteChar[index:index+messageSize].decode(), self.name)
          index += messageSize
          self.message.setTimeLeft(int.from_bytes(byteChar[index:index+4], 'big'))
          index += 4
       
    def getName(self):
       return self.name

    def setName(self, name):
       self.name = name
