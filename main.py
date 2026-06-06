import pygame, sys
from pygame.locals import *
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
player_turn = True


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

def minimax(position: Position, depth: int, maxingPlayer: bool):
    if depth == 0 or position.game_over:
        return position.eval_game_position()
     
    if maxingPlayer:
        maxEval = float("-inf")
        vis = set()
         
        for i, j in position.moves:
            for di, dj in DIRECTIONS:
                ni, nj = di + i, dj + j
                if (ni, nj) in vis or (ni, nj) in position.moves: continue
                position.position[ni][nj] = 1 # maxing is black
                
                
                move, eval = minimax()
                     
                 
             
             
         
         
        return maxEval
         
    else:
        minEval = float("inf")
        
        
        return minEval
    
    


def init_minimax():
    
    move, eval = minimax(board.position, MAX_SEARCH_DEPTH, True)
    

    
    
def main():

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()   
            
            if player_turn:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos

                    if (0 < int(mouse_x / TILE_SIZE) <= BOARD_SIZE) and (0 < int(mouse_y / TILE_SIZE) <= BOARD_SIZE):
                        j, i = board.snap_to_board(mouse_x, mouse_y)
                        if board.board[i][j] == -1:
                            board.place_white_piece(i, j)
                            print(board.check_win_con(i, j, player_turn))
                            player_turn = not player_turn
            else:
                ai_move_info = init_minimax()
                
                
                
                            
        



        board.draw(screen)

        pygame.display.update()

                
if __name__ == "__main__":
    main()

            

    
