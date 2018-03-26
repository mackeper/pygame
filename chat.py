from PyQt4 import QtGui, QtCore
from message import Message

class Chat:
    def __init__(self, x, y, width, height):
        self.messages = [Message('hej',"test1"), Message('macke','test2')]
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.newLine = ""

    def addMessage(self, message):
        self.messages.append(message)

    def draw(self, painter):
        painter.setPen(QtGui.QColor(0x450045))
        font = QtGui.QFont(QtGui.QFont('Decorative', 20))
        fontMetrics = QtGui.QFontMetrics(font)
        height = fontMetrics.height()
        painter.setFont(font)
        painter.drawText(self.x, self.y + self.height, '> ' + self.newLine)
        counter = 1
        for i in range(len(self.messages)-1, -1, -1):
            width = fontMetrics.boundingRect(self.messages[i].getString()).width()
            painter.drawText(self.x, self.y + self.height - height*counter, self.messages[i].getString())
            counter += 1

    def appendLetter(self, letter):
        self.newLine = self.newLine + letter

    def clearNewLine(self):
        self.newLine = ""
        
    def getNewLine(self):
        return self.newLine

    def update(self):
        pass
