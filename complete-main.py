import pygame, sys
from pygame.locals import *
from Board import Board


def main():
    BOARD_SIZE = 15

    TILE_SIZE = 40

    windowHeight = (BOARD_SIZE + 1) * TILE_SIZE
    windowWidth = (BOARD_SIZE + 1) * TILE_SIZE

    pygame.init()
    screen = pygame.display.set_mode((windowWidth, windowHeight))

    pygame.display.set_caption('Gomoku Game')


    board = Board(BOARD_SIZE, TILE_SIZE)


    player_turn = "w" # w/b

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()   
            if event.type == pygame.MOUSEBUTTONDOWN:
            
                #print(event.pos)``
                mouse_x, mouse_y = event.pos

                if (0 < int(mouse_x / TILE_SIZE) <= BOARD_SIZE) and (0 < int(mouse_y / TILE_SIZE) <= BOARD_SIZE):
                    j, i = board.snap_to_board(mouse_x, mouse_y)
                    if board.board[i][j] == -1:

                        if player_turn == 'w':
                            board.place_white_piece(i, j)
                            print(board.check_win_con(i, j, player_turn))
                            player_turn = 'b'
                        elif player_turn == 'b':
                            board.place_black_piece(i, j)
                            print(board.check_win_con(i, j, player_turn))
                            player_turn = 'w'


        board.draw(screen)

        pygame.display.update()

                
if __name__ == "__main__":
    main()

            

    
