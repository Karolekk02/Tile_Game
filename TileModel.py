class TileModel:
    def __init__(self, struct, color):
        self.struct = struct
        self.color = color
    def getWidth(self):
        return len(self.struct[0])
    def getHeight(self):
        return len(self.struct)
    def getStruct(self):
        return self.struct
    def getColor(self):
        return self.color