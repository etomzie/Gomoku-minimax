import pygame, sys
from pygame.locals import *

from copy import deepcopy
import math

from Utils.Board import Board
from Utils.Postition import Position

MAX_SEARCH_DEPTH = 6

BOARD_SIZE = 15

TILE_SIZE = 40

windowHeight = (BOARD_SIZE + 1) * TILE_SIZE
windowWidth = (BOARD_SIZE + 1) * TILE_SIZE

pygame.init()
screen = pygame.display.set_mode((windowWidth, windowHeight))

pygame.display.set_caption('Gomoku Game')


board = Board(BOARD_SIZE, TILE_SIZE)


DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

"""function minimax(position, depth, maximizingPlayer)
	if depth == 0 or game over in position
		return static evaluation of position
 
	if maximizingPlayer
		maxEval = -infinity
		for each child of position
			eval = minimax(child, depth - 1, false)
			maxEval = max(maxEval, eval)
		return maxEval
 
	else
		minEval = +infinity
		for each child of position
			eval = minimax(child, depth - 1, true)
			minEval = min(minEval, eval)
		return minEval
 
 
// initial call
minimax(currentPosition, 3, true)
"""

def minimax(pos: Position, depth: int, maxingPlayer: bool):
    over = pos.game_over()
    if depth == 0 or over:
        return pos.static_eval_position(over)

    if pos.prev_i == -1 and pos.prev_j == -1:
        return 
    
    best_move = (-1, -1)


    if maxingPlayer:
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
                now_pos.player_turn = True
                

                move, eval = minimax(now_pos, depth - 1, not maxingPlayer)
                if eval > maxEval:
                    best_move = move
                    maxEval = eval

        return best_move, maxEval


         
    else:
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
                now_pos.player_turn = False
                
                

                move, eval = minimax(now_pos, depth - 1, not maxingPlayer)
                if eval < minEval:
                    best_move = move
                    minEval = eval

        return best_move, minEval
        
    
    


def init_minimax():
    
    move, eval = minimax(board.position, MAX_SEARCH_DEPTH, True)
    

    
    
def main():

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()   
            
            if board.player_turn:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos

                    if (0 < int(mouse_x / TILE_SIZE) <= BOARD_SIZE) and (0 < int(mouse_y / TILE_SIZE) <= BOARD_SIZE):
                        j, i = board.snap_to_board(mouse_x, mouse_y)
                        if board.position[i][j] == -1:
                            board.place_white_piece(i, j)
                            board.player_turn = False

    
            else:
                ai_move_info = init_minimax()


                board.player_turn = True
                
                
                
                            
        



        board.draw(screen)

        pygame.display.update()

                
if __name__ == "__main__":
    main()

            

    
