import pygame, sys
from pygame.locals import *
from Utils.Postition import Position

import random





class Board(Position):
    def __init__(self, BOARD_SIZE, TILE_SIZE):
        super().__init__(BOARD_SIZE, TILE_SIZE)


    def place_black_piece(self, i, j):
        self.position[i][j] = 1
    def place_white_piece(self, i, j):
        self.position[i][j] = 2

        
    def console_check(self,):
        print(*self.position, sep = '\n') 
        print()   
    

    

    def snap_to_board(self, x, y):
        return round(x / self.TILE_SIZE) - 1, round(y / self.TILE_SIZE) - 1


    def draw(self, screen):
        screen.fill("#f8d182")

        for i in range(self.BOARD_SIZE - 1):
            for j in range(self.BOARD_SIZE - 1):
                if i != self.BOARD_SIZE and j != self.BOARD_SIZE:
                    pygame.draw.rect(screen, (0, 0, 0), (self.TILE_SIZE * (i + 1), self.TILE_SIZE * (j + 1), self.TILE_SIZE + 1, self.TILE_SIZE + 1), width = 2)
        
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.position[i][j] == 1:
                    pygame.draw.circle(screen, (0 ,0 , 0), ((j + 1) * self.TILE_SIZE, (i + 1) * self.TILE_SIZE), self.TILE_SIZE / 2 - 1)
                elif self.position[i][j] == 2:
                    pygame.draw.circle(screen, (255 ,255 , 255), ((j + 1) * self.TILE_SIZE, (i + 1) * self.TILE_SIZE), self.TILE_SIZE / 2 - 1)


        