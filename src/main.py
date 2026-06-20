import pygame, sys
from pygame.locals import *

from copy import deepcopy
import math

from Utils.board import Board
from Utils.position import Position
from settings import GameSettings
from evaluator import Evaluator

pygame.init()

MAX_SEARCH_DEPTH = GameSettings.MAX_SEARCH_DEPTH
BOARD_SIZE = GameSettings.BOARD_SIZE
TILE_SIZE = GameSettings.TILE_SIZE
windowHeight = GameSettings.SCREEN_HEIGHT
windowWidth = GameSettings.SCREEN_WIDTH


screen = pygame.display.set_mode((windowWidth, windowHeight))

pygame.display.set_caption(GameSettings.TITLE)


board = Board(BOARD_SIZE, TILE_SIZE)

EVALUATOR = Evaluator()
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

"""TODO
represent board with bitmask of size 15 * 15


"""



def minimax(pos: Position, depth: int, maxingPlayer: bool):
    if pos.is_game_over():
        if pos.turn == 'W': # White to move: white lost
            return float("-inf") 
        else:
            return float("inf")

    if depth == 0:
        return EVALUATOR.static_eval(pos)

    if pos.prev_i == -1 and pos.prev_j == -1:
        return 
    
    best_move = (-1, -1)


    if maxingPlayer: # WHITE
        maxEval = float("-inf")
        vis = set()
         
        for i, j in pos.moves:
            for di, dj in DIRECTIONS:
                ni, nj = di + i, dj + j
                if not(0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE): continue
                if (ni, nj) in vis: continue
                if pos.position[ni][nj] != -1: continue

                now_pos = deepcopy(pos)
                now_pos.position[ni][nj] = 1 # maxing black
                now_pos.moves.add((ni, nj))
                now_pos.prev_i = ni
                now_pos.prev_j = nj
                now_pos.turn = 'B'
                

                move, eval = minimax(now_pos, depth - 1, not maxingPlayer)
                if eval > maxEval:
                    best_move = move
                    maxEval = eval

        return best_move, maxEval


         
    else: # BLACK
        minEval = float("inf")

        vis = set()
         
        for i, j in pos.moves:
            for di, dj in DIRECTIONS:
                ni, nj = di + i, dj + j
                if not(0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE): continue
                if (ni, nj) in vis: continue
                if pos.position[ni][nj] != -1: continue

                now_pos = deepcopy(pos)
                now_pos.position[ni][nj] = 1 # maxing black
                now_pos.moves.add((ni, nj))
                now_pos.prev_i = ni
                now_pos.prev_j = nj
                now_pos.turn = "W"
                
                

                move, eval = minimax(now_pos, depth - 1, not maxingPlayer)
                if eval < minEval:
                    best_move = move
                    minEval = eval

        return best_move, minEval
        
    
    


def init_minimax():
    
    move, eval = minimax(board.position, MAX_SEARCH_DEPTH, True)
    print(move)
    return move
    

    
    
def main():

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()   
            
            if board.turn == GameSettings.PLAYER:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos

                    if (0 < int(mouse_x / TILE_SIZE) <= BOARD_SIZE) and (0 < int(mouse_y / TILE_SIZE) <= BOARD_SIZE):
                        j, i = board.snap_to_board(mouse_x, mouse_y)
                        if board.position[i][j] == -1:
                            board.place_white_piece(i, j)
                            board.turn = GameSettings.AI

    
            else:
                ai_move_info = init_minimax()


                board.turn = GameSettings.PLAYER
                
                
                
                            
        



        board.draw(screen)

        pygame.display.update()

                
if __name__ == "__main__":
    main()

            

    
