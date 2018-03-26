class World():
    def __init__(self, width = 1280, height = 720):
        self.character = None
        self.entities = []
        self.otherPlayers = []

        self.width = width
        self.height = height

    def setSize(self, width, height):
        self.width = width
        self.height = height

    def getSize(self):
        return (width, height)

    def setCharacter(self, c):
        self.character = c
    
    def getCharacter(self):
        return self.character

    def setEntities(self, es):
        self.entities = es

    def addEntity(self, e):
        self.entities.append(e)

    def getEntities(self):
        return self.entities

    def setOtherPlayers(self, ops):
        self.otherPlayers = ops

    def addOtherPlayer(self, op):
        self.otherPlayers.append(op)

    def getOtherPlayers(self):
        return self.otherPlayers
