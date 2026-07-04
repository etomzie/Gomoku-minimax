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



    
    def five_in_direction(self, dx, dy, chk_state):
        count = 1

        i, j = self.prev_i + dx, self.prev_j + dy
        while 0 <= i < BS and 0 <= j < BS and self.position[i][j] == chk_state:
            count += 1
            i += dx
            j += dy

        i, j = self.prev_i - dx, self.prev_j - dy
        while 0 <= i < BS and 0 <= j < BS and self.position[i][j] == chk_state:
            count += 1
            i -= dx
            j -= dy

        return count >= 5
    
        
    
    
    def is_game_over(self):
        if self.turn == GameSettings.PLAYER:
            chk_state = GameSettings.AI
        else:
            chk_state = GameSettings.PLAYER
        
        return (
            self.five_in_direction(1, 0, chk_state) or
            self.five_in_direction(0, 1, chk_state) or
            self.five_in_direction(1, 1, chk_state) or
            self.five_in_direction(1, -1, chk_state)
        )
         
            
