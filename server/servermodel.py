class ServerModel:
    def __init__(self):
        self.characters = {}
        self.entities = {}
        self.messages = {}

    #c as bytearray
    def addCharacter(self, id, c):
        self.characters[id] = c
    
    #e as bytearray
    def addEntity(self, id, e):
        pass

    #m as bytearray
    def addMessage(self, id, m):
        pass

    def getCharacters(self):
        return self.characters

    def getEntities(self):
        return self.entities

    def getMessages(self):
        return self.messages

    
