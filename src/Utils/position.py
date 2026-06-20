from settings import GameSettings

class Position():
    def __init__(self, BOARD_SIZE, TILE_SIZE):

        self.BOARD_SIZE = BOARD_SIZE
        self.TILE_SIZE = TILE_SIZE
        
        self.moves = set()
        self.position = [['.'] * (BOARD_SIZE) for _ in range((BOARD_SIZE))]
        
        self.prev_i = -1
        self.prev_j = -1

        self.turn = GameSettings.PLAYER



    
    
        
    
    
    def is_game_over(self):
        if self.turn == GameSettings.PLAYER:
            chk_state = GameSettings.AI
        else:
            chk_state = GameSettings.PLAYER

        in_row = 0
        for i in range(max(0, self.prev_i - 5), min(self.BOARD_SIZE - 1, self.prev_i + 5)):
            if self.position[i][self.prev_j] == chk_state:
                in_row += 1
            else:
                in_row = 0
            
            if in_row == 5:
                return True
        in_row = 0
        for j in range(max(0, self.prev_j - 5), min(self.BOARD_SIZE - 1, self.prev_j + 5)):
            if self.position[self.prev_i][j] == chk_state:
                in_row += 1
            else:
                in_row = 0
            
            if in_row == 5:
                return True
            
        in_row = 0
        i = max(0, self.prev_i - 5)
        for j in range(max(0, self.prev_j - 5), min(self.BOARD_SIZE - 1, self.prev_j + 5)):
            if self.position[i][j] == chk_state:
                in_row += 1
            else:
                in_row = 0
            
            if in_row == 5:
                return True            
            i += 1
            if i >= self.BOARD_SIZE:
                break


        in_row = 0
        i = min(self.BOARD_SIZE - 1, self.prev_i + 5)
        for j in range(max(0, self.prev_j - 5), min(self.BOARD_SIZE - 1, self.prev_j + 5)):
            if self.position[i][j] == chk_state:
                in_row += 1
            else:
                in_row = 0
            
            if in_row == 5:
                return True            
            i -= 1
            if i < 0:
                break


        return False
         
            
