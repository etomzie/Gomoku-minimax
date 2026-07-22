import pygame, sys
from pygame.locals import *

from copy import deepcopy
import math
import random
from sys import stdout
import threading
import time

from Utils.board import Board
from Utils.position import Position
from settings import GameSettings
from evaluator import Evaluator
from eval_bar import Eval_Bar

pygame.init()

MAX_SEARCH_DEPTH = GameSettings.MAX_SEARCH_DEPTH
CHECK_RADIUS = GameSettings.CHECK_RADIUS
BOARD_SIZE = GameSettings.BOARD_SIZE
TILE_SIZE = GameSettings.TILE_SIZE
windowHeight = GameSettings.SCREEN_HEIGHT
windowWidth = GameSettings.SCREEN_WIDTH


offset = 40
screen = pygame.display.set_mode((windowWidth, windowHeight + offset))

pygame.display.set_caption(GameSettings.TITLE)
board_img = pygame.image.load("assests/board.png").convert()
board_img = pygame.transform.scale(board_img, (windowWidth - TILE_SIZE * 2, windowHeight - offset - TILE_SIZE))

board = Board(board_img)
EVALUATOR = Evaluator()
evalBar = Eval_Bar()


DIRECTIONS = []
for i in range(CHECK_RADIUS * -1, CHECK_RADIUS + 1):
    for j in range(CHECK_RADIUS * -1, CHECK_RADIUS + 1):
        if i == 0 and j == 0:
            continue
        DIRECTIONS.append((i, j))
print(DIRECTIONS)
D4 = [
    (0,1),
    (1,0),   
    (1,1),  
    (1,-1)   
]


engine_thinking = False
engine_move = None


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
        return (pos.prev_i, pos.prev_j), pos.score

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
            old_score = 0

            for di,dj in D4:
                line = EVALUATOR.get_line(pos.position, ni, nj, di, dj)
                old_score += EVALUATOR.evaluate_line(line)
            
            pos.position[ni][nj] = WHITE
            
            new_score = 0

            for di,dj in D4:
                line = EVALUATOR.get_line(pos.position, ni, nj, di, dj)
                new_score += EVALUATOR.evaluate_line(line)
            pos.score += new_score - old_score
            
            
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
            pos.position[ni][nj] = EMPTY
            pos.score -= new_score - old_score
            
            
            pos.zobrist_hash ^= get_zobrist_value(ni, nj, WHITE)
            
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
            old_score = 0

            for di,dj in D4:
                line = EVALUATOR.get_line(pos.position, ni, nj, di, dj)
                old_score += EVALUATOR.evaluate_line(line)
                
            pos.position[ni][nj] = BLACK
            
            new_score = 0

            for di,dj in D4:
                line = EVALUATOR.get_line(pos.position, ni, nj, di, dj)
                new_score += EVALUATOR.evaluate_line(line)
            pos.score += new_score - old_score
            
            
            pos.zobrist_hash ^= get_zobrist_value(ni, nj, BLACK)
            pos.moves.add((ni, nj))
            old_turn = pos.turn
            old_i = pos.prev_i
            old_j = pos.prev_j

            pos.turn = WHITE
            pos.prev_i = ni
            pos.prev_j = nj

            _, eval = minimax(pos, depth-1, True, alpha, beta)

            # undop
            pos.position[ni][nj] = EMPTY
            pos.score -= new_score - old_score
            
            pos.zobrist_hash ^= get_zobrist_value(ni, nj, BLACK)
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
    global transposition
    transposition.clear()
    
    maxing = True if board.position.turn == WHITE else False
    move, eval = minimax(deepcopy(board.position), MAX_SEARCH_DEPTH, maxing)
    

    
    print(move, eval)
    

    
    return move
    
    
def start_engine_search():
    global engine_move, engine_thinking
    
    engine_move = init_minimax()
    engine_thinking = False


def main():
    global engine_move, engine_thinking
    
    IS_GAME_OVER = False
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()   
            if IS_GAME_OVER: continue
            
            if board.position.turn == GameSettings.PLAYER:
                if event.type == pygame.MOUSEBUTTONDOWN and not engine_thinking:
                    mouse_x, mouse_y = event.pos
                    mouse_y -= offset
                    

                    if (0 < int(mouse_x / TILE_SIZE) <= BOARD_SIZE) and (0 < int(mouse_y / TILE_SIZE) <= BOARD_SIZE):
                        j, i = board.snap_to_board(mouse_x, mouse_y)

                        if board.position.position[i][j] == EMPTY:
                            if GameSettings.PLAYER == BLACK:
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
                 if not engine_thinking:
                    engine_thinking = True

                    engine = threading.Thread(target = start_engine_search)
                    engine.start()
                    
                    
                    engine.join()
                    i, j = engine_move
                    
                    if GameSettings.AI == "B":
                        board.place_black_piece(i, j)
                    else:
                        board.place_white_piece(i, j)

                    board.position.prev_i = i
                    board.position.prev_j = j
                    board.position.moves.add((i, j))

                    board.position.turn = GameSettings.PLAYER
                    
                    evalBar.score = EVALUATOR.static_eval(board.position)
                    
                    engine_move = None
                    
                    
        if board.position.is_game_over():
            #board.end_game()
            IS_GAME_OVER = True
            #exit()
                
                
                
                            
        

        board.draw(screen)
        evalBar.draw(screen)

        pygame.display.update()

                
if __name__ == "__main__":
    main()

            

    
