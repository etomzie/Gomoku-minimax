import pygame, sys
from pygame.locals import *

from Utils.position import Position
from settings import GameSettings


import random

EMPTY = '.'
WHITE = 'W'
BLACK = 'B'


class Board():
    def __init__(self):
        self.position = Position()


    def place_black_piece(self, i, j):
        self.position.position[i][j] = 'B'
    def place_white_piece(self, i, j):
        self.position.position[i][j] = 'W'

        
    def console_check(self,):
        print(*self.position.position, sep = '\n') 
        print()   
    

    

    def snap_to_board(self, x, y):
        return round(x / GameSettings.TILE_SIZE) - 1, round(y / GameSettings.TILE_SIZE) - 1


    def draw(self, screen):
        screen.fill("#f8d182")
        
        BS = GameSettings.BOARD_SIZE
        TS = GameSettings.TILE_SIZE

        for i in range(BS - 1):
            for j in range(BS - 1):
                if i != BS and j != BS:
                    pygame.draw.rect(screen, (0, 0, 0), (TS * (i + 1), TS * (j + 1), TS + 1, TS + 1), width = 2)
        
        for i in range(BS):
            for j in range(BS):
                if self.position.position[i][j] == BLACK:
                    pygame.draw.circle(screen, (0 ,0 , 0), ((j + 1) * TS, (i + 1) * TS), TS / 2 - 1)
                elif self.position.position[i][j] == WHITE:
                    pygame.draw.circle(screen, (255 ,255 , 255), ((j + 1) * TS, (i + 1) * TS), TS / 2 - 1)

    def end_game(self):
        if self.position.turn == BLACK:
            print("WHITE WINS")

        elif self.position.turn == WHITE:
            print("BLACK WINS")
        else:
            print("DRAW")

    def draw_GameOver(self, screen):
        screen.fill(255, 255, 255)
        

        