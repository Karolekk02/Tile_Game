import math
import random
import pygame
from Structures import Board
from TileModel import TileModel
from TileTypes import tiles, colors
from TileGroups import RectangleObject, GroupObject


class Game:

    def __init__(self):
        pygame.init()
        self.is_running = True
        self.game_over = False
        self.TICK = 120
        self.mouse = pygame.mouse.get_pos()
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Tile Game")
        self.screen_width = self.window.get_width()
        self.screen_height = self.window.get_height()
        self.board_cell_size = 50
        self.clock = pygame.time.Clock()

        self.tileTypes = tiles
        self.colorTypes = colors
        self.board = self.createBoard()
        self.availableTiles = [None for i in range(3)]
        self.table_tiles = [None for i in range(3)]
        self.activeTile = None

        while self.is_running:
            self.update()

        pygame.quit()
    
    def createBoard(self):
        start_x = (self.screen_width - 8 * self.board_cell_size) // 2
        start_y = (self.screen_height - 8 * self.board_cell_size) // 4
        group = [[None for i in range (8)] for i in range(8)]
        color = (255, 255, 255)
        for col_idx in range(8):
            for row_idx in range(8):
                x = start_x + row_idx * self.board_cell_size
                y = start_y + col_idx * self.board_cell_size
                group[col_idx][row_idx] = RectangleObject(x, y, row_idx, col_idx, self.board_cell_size, color)
        return Board(group)

    def drawAvailableTiles(self):
        for tile in self.availableTiles:
            if tile != None:
                tile.draw(self.window)
    
    def drawBoard(self):
        self.board.draw(self.window)

    def convert_to_array(self, tile):
        rows = tile.strip().split('\n')
        return [[int(char) for char in row.strip()] for row in rows]
    
    def getNewTile(self):
        newTile = random.choice(random.choice(self.tileTypes))
        newColor = random.choice(self.colorTypes)
        return TileModel(self.convert_to_array(newTile), newColor)

    def placeTile(self):
        tmp = self.availableTiles[self.activeTile].get_rect().topleft
        collideId = self.board.collideId((tmp[0] + 25, tmp[1] + 25))

        if collideId is not None:
            if self.board.checkTile(self.table_tiles[self.activeTile], collideId[0], collideId[1]):
                self.board.addTile(self.table_tiles[self.activeTile], collideId[0], collideId[1])
                self.availableTiles[self.activeTile] = None
                self.table_tiles[self.activeTile] = None
        if self.availableTiles[self.activeTile] is not None:
            self.availableTiles[self.activeTile].reset()

    def newTiles(self):
        for i in range(3):
            self.table_tiles[i] = self.getNewTile()

        total_width = sum(len(board.getStruct()[0]) * self.board_cell_size for board in self.table_tiles) + 2 * self.board_cell_size
        start_x = (self.screen_width - total_width) // 2
        start_y = self.screen_height - (6 * self.board_cell_size)

        x_offset = start_x
        y_offset = start_y

        for idx, tile in enumerate(self.table_tiles):
            board = tile.getStruct()
            board_width = len(board[0])
            group = []
            for y, row in enumerate(board):
                for x, cell in enumerate(row):
                    x_pos = x_offset + x * self.board_cell_size
                    y_pos = y_offset + y * self.board_cell_size

                    
                    if cell != 0:
                        color = tile.getColor()
                        group.append(RectangleObject(x_pos, y_pos, x, y, self.board_cell_size, color))

            x_offset += ((board_width + 1) * self.board_cell_size)
            self.availableTiles[idx] = GroupObject(group)

    def update(self):
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for num, tile in enumerate(self.availableTiles):
                        if tile is not None and tile.collidepoint(event.pos):
                            self.activeTile = num
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.activeTile is not None:
                    self.placeTile()
                    self.activeTile = None
            if event.type == pygame.MOUSEMOTION:
                if self.activeTile != None:
                    self.availableTiles[self.activeTile].move(event.rel)
                    

        if self.availableTiles[0] == None and self.availableTiles[1] == None and self.availableTiles[2] == None:
            self.newTiles()
        for tile in self.table_tiles:
            if tile != None and not self.board.checkPlace(tile):
                # self.is_running = False
                print("looser")
        self.board.checkComplete()
        self.window.fill((255, 255, 255))
        self.drawBoard()
        self.drawAvailableTiles()


if __name__ == '__main__':
    Game()
