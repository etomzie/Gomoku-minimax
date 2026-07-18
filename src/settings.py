
class Settings:            
    TITLE  = "Gomoku Game"    
    DEBUG = True
    TILE_SIZE: int = 40
    BOARD_SIZE = 15
    SCREEN_WIDTH = (BOARD_SIZE + 1) * TILE_SIZE
    SCREEN_HEIGHT = (BOARD_SIZE + 1) * TILE_SIZE 
    MAX_SEARCH_DEPTH = 3
    CHECK_RADIUS = 2

    PLAYER = 'W'
    AI = 'B'

GameSettings = Settings()