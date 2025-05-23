import pygame

class Board:
    def __init__(self, objects):
        self.objects = objects
        self.update_rect()
        self.default_color = (255, 255, 255)

    def update_rect(self):
        self.rect = self.objects[0][0].get_rect()
        for row in self.objects:
            for obj in row:
                self.rect = self.rect.union(obj.get_rect())

    def get_rect(self):
        return self.rect
    
    def collidepoint(self, pos):
        if self.rect.collidepoint(pos):
            for row in self.objects:
                for obj in row:
                    if obj.get_rect().collidepoint(pos):
                        return True
        return False
    
    def collideId(self, pos):
        if self.rect.collidepoint(pos):
            for y_id, row in enumerate(self.objects):
                for x_id, obj in enumerate(row):
                    if obj.get_rect().collidepoint(pos):
                        return (x_id, y_id)
        return None
    
    def addTile(self, tile, x, y):
        new_tile = tile.getStruct()
        new_color = tile.getColor()
        for i in range(tile.getHeight()):
            for j in range(tile.getWidth()):
                if new_tile[i][j] != 0:
                    self.objects[y+i][x+j].changeColor(new_color)

    def checkTile(self, tile, x, y):
        new_tile = tile.getStruct()
        if y + tile.getHeight() > 8 or x + tile.getWidth() > 8:
            return False
        for i in range(tile.getHeight()):
            for j in range(tile.getWidth()):
                if self.objects[y+i][x+j].getColor() != self.default_color and new_tile[i][j] != 0:
                    return False
        return True
    
    def checkComplete(self):
        cols = self.checkCols()
        rows = self.checkRows()
        if rows is not None:
            for row in rows:
                for obj in range(8):
                    self.objects[row][obj].changeColor(self.default_color)
        if cols is not None:
            for col in cols:
                for obj in range(8):
                    self.objects[obj][col].changeColor(self.default_color)

    def checkRows(self):
        res = []
        for row_id, row in enumerate(self.objects):
            full = 1
            for obj in row:
                if obj.getColor() == self.default_color:
                    full = 0
                    break
            if full:
                res.append(row_id)
        return res

    def checkCols(self):
        res = []
        for x in range(8):
            full = True
            for y in range(8):
                if self.objects[y][x].getColor() == self.default_color:
                    full = False
                    break
            if full:
                res.append(x)
        return res
            
    
    def checkPlace(self, tile):
        new_tile = tile.getStruct()
        for y in range(8 - tile.getHeight()):
            for x in range(8 - tile.getWidth()):
                if self.checkTile(tile, x, y):
                    return True
        return False
    
    def draw(self, surface):
        for row in self.objects:
            for obj in row:
                obj.draw(surface)
