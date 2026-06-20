from settings import GameSettings

BS = GameSettings.BOARD_SIZE
TS = GameSettings.TILE_SIZE

class Position():
    def __init__(self):


        self.moves = set()
        self.position = [['.'] * (BS) for _ in range((BS))]
        
        self.prev_i = -1
        self.prev_j = -1

        self.turn = GameSettings.PLAYER



    
    
        
    
    
    def is_game_over(self):
        if self.turn == GameSettings.PLAYER:
            chk_state = GameSettings.AI
        else:
            chk_state = GameSettings.PLAYER

        in_row = 0
        for i in range(max(0, self.prev_i - 5), min(BS - 1, self.prev_i + 5)):
            if self.position[i][self.prev_j] == chk_state:
                in_row += 1
            else:
                in_row = 0
            
            if in_row == 5:
                return True
        in_row = 0
        for j in range(max(0, self.prev_j - 5), min(BS - 1, self.prev_j + 5)):
            if self.position[self.prev_i][j] == chk_state:
                in_row += 1
            else:
                in_row = 0
            
            if in_row == 5:
                return True
            
        in_row = 0
        i = max(0, self.prev_i - 5)
        for j in range(max(0, self.prev_j - 5), min(BS - 1, self.prev_j + 5)):
            if self.position[i][j] == chk_state:
                in_row += 1
            else:
                in_row = 0
            
            if in_row == 5:
                return True            
            i += 1
            if i >= BS:
                break


        in_row = 0
        i = min(BS - 1, self.prev_i + 5)
        for j in range(max(0, self.prev_j - 5), min(BS - 1, self.prev_j + 5)):
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
         
            
