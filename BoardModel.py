from TileModel import TileModel

class BoardModel:
    def __init__(self):
        self.board = [[0 for x in range(8)] for y in range(8)]

    def addTile(self, tile, x, y):
        new_tile = tile.getStruct()
        new_color = tile.getColor()
        for i in range(tile.getHeight()):
            for j in range(tile.getWidth()):
                if new_tile[i][j] != 0:
                    self.board[y+i][x+j] = new_color

    def checkTile(self, tile, x, y):
        new_tile = tile.getStruct()
        if y + tile.getHeight() >= 8 or x + tile.getWidth() >= 8:
            return False
        for i in range(tile.getHeight()):
            for j in range(tile.getWidth()):
                if self.board[y+i][x+j] != 0 and new_tile[i][j] != 0:
                    return False
        return True
    
    def checkComplete(self):
        self.checkCols()
        self.checkRows()

    def checkRows(self):
        for row in self.board:
            if not 0 in row:
                row = [0 for i in range(8)]

    def checkCols(self):
        for x in range(8):
            full = True
            for y in range(8):
                if self.board[y][x] == 0:
                    full = False
                    break
            if full:
                for y in range(8):
                    self.board[y][x] = 0
    
    def checkPlace(self, tile):
        new_tile = tile.getStruct()
        for y in range(8 - tile.getHeight()):
            for x in range(8 - tile.getWidth()):
                if self.checkTile(tile, x, y):
                    return True
        return False

    def getBoard(self):
        return self.board
    