import pygame

class GroupObject:
    def __init__(self, objects):
        self.objects = objects
        self.update_rect()

    def update_rect(self):
        self.rect = self.objects[0].get_rect()
        for obj in self.objects[1:]:
            self.rect = self.rect.union(obj.get_rect())

    def get_rect(self):
        return self.rect
    
    def collidepoint(self, pos):
        if self.rect.collidepoint(pos):
            for obj in self.objects:
                if obj.get_rect().collidepoint(pos):
                    return True
        return False
    
    def collideId(self, pos):
        if self.rect.collidepoint(pos):
            for obj in self.objects:
                if obj.get_rect().collidepoint(pos):
                    return obj.get_tileId()
        return None
    
    def compareAndSetColor(self, pos, color):
        for obj in self.objects:
            if obj.get_tileId == pos:
                obj.changeColor(color)

    def draw(self, surface):
        for obj in self.objects:
            obj.draw(surface)

    def move(self, pos):
        for obj in self.objects:
            obj.move(pos)
        self.update_rect()

    def reset(self):
        for obj in self.objects:
            obj.reset()
        self.update_rect()


class RectangleObject:
    def __init__(self, pos_x, pos_y, x, y, a, color):
        self.def_pos = (pos_x, pos_y)
        self.rect = pygame.Rect(pos_x, pos_y, a, a)
        self.color = color
        self.tileId = (x, y)

    def get_rect(self):
        return self.rect
    
    def get_tileId(self):
        return self.tileId
    
    def changeColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, "BLACK", self.rect, 1)

    def move(self, pos):
        self.rect.x += pos[0]
        self.rect.y += pos[1]

    def reset(self):
        self.rect.x = self.def_pos[0]
        self.rect.y = self.def_pos[1]