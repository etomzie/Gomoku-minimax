import pygame, sys
from pygame.locals import *
import random





class Board():
    def __init__(self, BOARD_SIZE, TILE_SIZE):
        self.BOARD_SIZE = BOARD_SIZE
        self.TILE_SIZE = TILE_SIZE

        self.board = [[-1] * (BOARD_SIZE + 2) for _ in range((BOARD_SIZE + 2))]


    def place_black_piece(self, i, j):
        self.board[i][j] = 1
    def place_white_piece(self, i, j):
        self.board[i][j] = 2

    def check_win_con(self, prev_i, prev_j, side: str):
        if side == 'b':
            chk_state = 1
        elif side == 'w':
            chk_state = 2

        in_row = 0
        for i in range(max(0, prev_i - 5), min(self.BOARD_SIZE - 1, prev_i + 5)):
            if self.board[i][prev_j] == chk_state:
                in_row += 1
            else:
                in_row = 0
            
            if in_row == 5:
                return True
        in_row = 0
        for j in range(max(0, prev_j - 5), min(self.BOARD_SIZE - 1, prev_j + 5)):
            if self.board[prev_i][j] == chk_state:
                in_row += 1
            else:
                in_row = 0
            
            if in_row == 5:
                return True
            
        in_row = 0
        i = max(0, prev_i - 5)
        for j in range(max(0, prev_j - 5), min(self.BOARD_SIZE - 1, prev_j + 5)):
            if self.board[i][j] == chk_state:
                in_row += 1
            else:
                in_row = 0
            
            if in_row == 5:
                return True            
            i += 1
            if i >= self.BOARD_SIZE:
                break


        in_row = 0
        i = min(self.BOARD_SIZE - 1, prev_i + 5)
        for j in range(max(0, prev_j - 5), min(self.BOARD_SIZE - 1, prev_j + 5)):
            if self.board[i][j] == chk_state:
                in_row += 1
            else:
                in_row = 0
            
            if in_row == 5:
                return True            
            i -= 1
            if i < 0:
                break


        return False

    def snap_to_board(self, x, y):
        return round(x / self.TILE_SIZE), round(y / self.TILE_SIZE)


    def draw(self, screen):
        screen.fill("#f8d182")

        for i in range(1, self.BOARD_SIZE + 1):
            for j in range(1, self.BOARD_SIZE + 1):
                if i != self.BOARD_SIZE and j != self.BOARD_SIZE:
                    pygame.draw.rect(screen, (0, 0, 0), (self.TILE_SIZE * i, self.TILE_SIZE * j, self.TILE_SIZE + 1, self.TILE_SIZE + 1), width = 2)
        
        for i in range(1, self.BOARD_SIZE + 1):
            for j in range(1, self.BOARD_SIZE + 1):
                if self.board[i][j] == 1:
                    pygame.draw.circle(screen, (0 ,0 , 0), (j * self.TILE_SIZE, i * self.TILE_SIZE), self.TILE_SIZE / 2 - 1)
                elif self.board[i][j] == 2:
                    pygame.draw.circle(screen, (255 ,255 , 255), (j * self.TILE_SIZE, i * self.TILE_SIZE), self.TILE_SIZE / 2 - 1)


        