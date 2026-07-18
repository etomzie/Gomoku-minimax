import pygame, sys
from pygame.locals import *

from copy import deepcopy
import math
import random
from sys import stdout

from Utils.board import Board
from Utils.position import Position
from settings import GameSettings
from evaluator import Evaluator

pygame.init()

MAX_SEARCH_DEPTH = GameSettings.MAX_SEARCH_DEPTH
CHECK_RADIUS = GameSettings.CHECK_RADIUS
BOARD_SIZE = GameSettings.BOARD_SIZE
TILE_SIZE = GameSettings.TILE_SIZE
windowHeight = GameSettings.SCREEN_HEIGHT
windowWidth = GameSettings.SCREEN_WIDTH


screen = pygame.display.set_mode((windowWidth, windowHeight))

pygame.display.set_caption(GameSettings.TITLE)


board = Board()

EVALUATOR = Evaluator()


DIRECTIONS = []
for i in range(CHECK_RADIUS * -1, CHECK_RADIUS + 1):
    for j in range(CHECK_RADIUS * -1, CHECK_RADIUS + 1):
        if i == 0 and j == 0:
            continue
        DIRECTIONS.append((i, j))
print(DIRECTIONS)





EMPTY = '.'
WHITE = 'W'
BLACK = 'B'

random.seed(0)

ZOBRIST = [
    [
        [
            random.getrandbits(64) for _ in range(2)
        ]
        for _ in range(BOARD_SIZE)
    ]
    for _ in range(BOARD_SIZE)
]


def get_zobrist_value(i, j, piece):
    if piece == WHITE:
        return ZOBRIST[i][j][0]
    else:
        return ZOBRIST[i][j][1]


"""TODO
represent board with bitmask of size 15 * 15

"""

transposition = {}




def minimax(pos: Position, depth: int, maxingPlayer: bool, 
            alpha=float("-inf"), beta=float("inf")):
    global transposition
    
    key = (
        pos.zobrist_hash,
        depth,
        maxingPlayer
    )
    if key in transposition:
        return transposition[key]


    if pos.is_game_over():
        winner = BLACK if pos.turn == WHITE else WHITE
        if winner == WHITE:
            transposition[key] = ((pos.prev_i, pos.prev_j), float("inf"))
            return (pos.prev_i, pos.prev_j), float("inf")
        else:
            transposition[key] = ((pos.prev_i, pos.prev_j), float("-inf"))
            return (pos.prev_i, pos.prev_j), float("-inf")


    if depth == 0:
        eval = EVALUATOR.static_eval(pos)
        transposition[key] = ((pos.prev_i, pos.prev_j), eval)

        return (pos.prev_i, pos.prev_j), eval

    if pos.prev_i == -1 and pos.prev_j == -1:
        result = ((BOARD_SIZE // 2, BOARD_SIZE // 2), 0)
        transposition[key] = result
        return result
    
    best_move = (-1, -1)


    if maxingPlayer: # WHITE
        maxEval = float("-inf")
        moves = set()

        for i, j in pos.moves:
            for di, dj in DIRECTIONS:
                ni, nj = i + di, j + dj
                if 0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE:
                    if pos.position[ni][nj] == EMPTY:
                        moves.add((ni, nj))

        moves = list(moves)
        moves.sort(key=lambda x: EVALUATOR.quick_eval_move(pos, x), reverse=True)

        for ni, nj in moves:        
                
            pos.position[ni][nj] = WHITE
            pos.zobrist_hash ^= get_zobrist_value(ni, nj, WHITE)
            pos.moves.add((ni, nj))
            old_turn = pos.turn
            old_i = pos.prev_i
            old_j = pos.prev_j

            pos.turn = BLACK
            pos.prev_i = ni
            pos.prev_j = nj

            _, eval = minimax(pos, depth-1, False, alpha, beta)

            # undo
            pos.zobrist_hash ^= get_zobrist_value(ni, nj, WHITE)
            pos.position[ni][nj] = EMPTY
            pos.moves.remove((ni, nj))

            pos.turn = old_turn
            pos.prev_i = old_i
            pos.prev_j = old_j
            
            if eval > maxEval:
                best_move = (ni, nj)
                maxEval = eval

            alpha = max(alpha, eval)

            if beta <= alpha:
                return best_move, maxEval


        transposition[key] = (best_move, maxEval)
        return best_move, maxEval      


         
    else: # BLACK
        minEval = float("inf")
        moves = set()

        for i, j in pos.moves:
            for di, dj in DIRECTIONS:
                ni, nj = i + di, j + dj
                if 0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE:
                    if pos.position[ni][nj] == EMPTY:
                        moves.add((ni, nj))

        moves = list(moves)
        moves.sort(key=lambda x: EVALUATOR.quick_eval_move(pos, x))

        for ni, nj in moves:
            pos.position[ni][nj] = BLACK
            pos.zobrist_hash ^= get_zobrist_value(ni, nj, BLACK)
            pos.moves.add((ni, nj))
            old_turn = pos.turn
            old_i = pos.prev_i
            old_j = pos.prev_j

            pos.turn = WHITE
            pos.prev_i = ni
            pos.prev_j = nj

            _, eval = minimax(pos, depth-1, True, alpha, beta)

            # undo
            pos.zobrist_hash ^= get_zobrist_value(ni, nj, BLACK)
            pos.position[ni][nj] = EMPTY
            pos.moves.remove((ni, nj))
            pos.turn = old_turn
            pos.prev_i = old_i
            pos.prev_j = old_j
            
            if eval < minEval:
                best_move = (ni, nj)
                minEval = eval

            beta = min(beta, eval)

            if beta <= alpha:
                return best_move, minEval

        transposition[key] = (best_move, minEval)
        return best_move, minEval 
    


def init_minimax():
    maxing = True if board.position.turn == 'W' else False
    prun_val = float('-inf') if maxing else float("inf")
    move, eval = minimax(board.position, MAX_SEARCH_DEPTH, maxing)
    print(move, eval)
    return move
    

    
    


def main():
    IS_GAME_OVER = False
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()   
            if IS_GAME_OVER: continue
            
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
                                board.position.zobrist_hash ^= get_zobrist_value(i, j, BLACK)
                            else:
                                board.place_white_piece(i, j)
                                board.position.zobrist_hash ^= get_zobrist_value(i, j, WHITE)

                            board.position.prev_i = i
                            board.position.prev_j = j
                            board.position.moves.add((i, j))
                            
                            board.position.turn = GameSettings.AI

    
            else:
                info_i, info_j = init_minimax()
                
                print(EVALUATOR.count)

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
            IS_GAME_OVER = True
            #exit()
                
                
                
                            
        

        board.draw(screen)
        # if not IS_GAME_OVER:
        #     board.draw(screen)
        # else:
        #     board.draw_GameOver(screen)

        pygame.display.update()

                
if __name__ == "__main__":
    main()

            

    
