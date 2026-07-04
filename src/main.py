import pygame, sys
from pygame.locals import *

from copy import deepcopy
import math
from sys import stdout

from Utils.Board import Board
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


board = Board()

EVALUATOR = Evaluator()
    
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), 
              (0, -1), (0, 1), 
              (1, -1), (1, 0), (1, 1)] 
EMPTY = '.'
WHITE = 'W'
BLACK = 'B'

"""TODO
represent board with bitmask of size 15 * 15
implement alphabeta

"""



def minimax(pos: Position, depth: int, maxingPlayer: bool):
    if pos.is_game_over():
        winner = BLACK if pos.turn == WHITE else WHITE
        print(f"Game over {pos.turn} {winner}")
        if winner == WHITE:
            return (pos.prev_i, pos.prev_j), float("inf")
        else:
            return (pos.prev_i, pos.prev_j), float("-inf")


    if depth == 0:
        #stdout.write("DEPTH = 0\n")
        return (pos.prev_i, pos.prev_j), EVALUATOR.static_eval(pos)

    if pos.prev_i == -1 and pos.prev_j == -1:
        #stdout.write("first move\n")
        return (BOARD_SIZE // 2, BOARD_SIZE // 2), 0
    
    best_move = (-1, -1)


    if maxingPlayer: # WHITE
        maxEval = float("-inf")
        vis = set()
         
        for i, j in pos.moves:
            for di, dj in DIRECTIONS:
                ni, nj = di + i, dj + j
                if not(0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE): continue
                if (ni, nj) in vis: continue
                if pos.position[ni][nj] != EMPTY: continue
                vis.add((ni, nj))
                
                pos.position[ni][nj] = WHITE
                pos.moves.add((ni, nj))
                old_turn = pos.turn
                old_i = pos.prev_i
                old_j = pos.prev_j

                pos.turn = BLACK
                pos.prev_i = ni
                pos.prev_j = nj

                _, eval = minimax(pos, depth-1, False)

                # undo
                pos.position[ni][nj] = EMPTY
                pos.moves.remove((ni, nj))

                pos.turn = old_turn
                pos.prev_i = old_i
                pos.prev_j = old_j
                
                
                if eval > maxEval:
                    best_move = (ni, nj)
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
                if pos.position[ni][nj] != EMPTY: continue
                vis.add((ni, nj))

                pos.position[ni][nj] = BLACK
                pos.moves.add((ni, nj))
                old_turn = pos.turn
                old_i = pos.prev_i
                old_j = pos.prev_j

                pos.turn = WHITE
                pos.prev_i = ni
                pos.prev_j = nj

                _, eval = minimax(pos, depth-1, True)

                # undo
                pos.position[ni][nj] = EMPTY
                pos.moves.remove((ni, nj))
                pos.turn = old_turn
                pos.prev_i = old_i
                pos.prev_j = old_j
                
                if eval < minEval:
                    best_move = (ni, nj)
                    minEval = eval

        return best_move, minEval
        
    
    


def init_minimax():
    maxing = True if board.position.turn == 'W' else False
    print(maxing)
    move, eval = minimax(board.position, MAX_SEARCH_DEPTH, maxing)
    print(move, eval)
    return move
    

    
    
def main():

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()   
            
            
            if board.position.turn == GameSettings.PLAYER:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    

                    if (0 < int(mouse_x / TILE_SIZE) <= BOARD_SIZE) and (0 < int(mouse_y / TILE_SIZE) <= BOARD_SIZE):
                        j, i = board.snap_to_board(mouse_x, mouse_y)
                        #board.console_check()
                        #print(i, j)
                        if board.position.position[i][j] == EMPTY:
                            if GameSettings.PLAYER == "B":
                                board.place_black_piece(i, j)
                            else:
                                board.place_white_piece(i, j)

                            board.position.prev_i = i
                            board.position.prev_j = j
                            board.position.moves.add((i, j))
                            
                            board.position.turn = GameSettings.AI

    
            else:
                info_i, info_j = init_minimax()
                if GameSettings.AI == "B":
                    board.place_black_piece(info_i, info_j)
                else:
                    board.place_white_piece(info_i, info_j)

                board.position.prev_i = info_i
                board.position.prev_j = info_j
                board.position.moves.add((info_i, info_j))
                
                #board.console_check()

                board.position.turn = GameSettings.PLAYER
            #board.console_check()
        if board.position.is_game_over():
            board.end_game()
            exit()
                
                
                
                            
        



        board.draw(screen)

        pygame.display.update()

                
if __name__ == "__main__":
    main()

            

    
