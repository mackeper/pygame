from PyQt4 import QtGui, QtCore
import time, math

MESSAGE_ID_COUNT = 0

class Message():
    def __init__(self, string, charname):
        self.id = 1#MESSAGE_ID_COUNT
        #MESSAGE_ID_COUNT += 1
        self.string = string
        self.charname = charname
        self.dieAt = int(round(time.time())) + len(self.string)/2
        self.dead = False

    def isDead(self):
        return self.dead

    def setTimeLeft(self, newtime):
        self.dieAt = int(round(time.time())) + newtime

    def getTimeLeft(self):
        return self.dieAt - int(round(time.time()))
        
    def update(self):
        if(int(round(time.time())) > self.dieAt):
            self.dead = True
    
    def draw(self, painter, x, y):
        painter.setPen(QtGui.QColor(0x450045))
        font = QtGui.QFont(QtGui.QFont('Decorative', 20))
        fontMetrics = QtGui.QFontMetrics(font)
        width = fontMetrics.boundingRect(self.string).width()
        painter.setFont(font)
        painter.drawText(x - width/2, y, self.string)

    def getString(self):
        return self.string

    def generateBytes(self):
        """
        PROTOCOL:

        4 bytes: id
        4
        """
