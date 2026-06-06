

class Position():
    def __init__(self, BOARD_SIZE, TILE_SIZE):

        self.BOARD_SIZE = BOARD_SIZE
        self.TILE_SIZE = TILE_SIZE
        
        self.moves = set()
        self.position = [[-1] * (BOARD_SIZE) for _ in range((BOARD_SIZE))]
        
        self.prev_i = -1
        self.prev_j = -1
        
    
    def eval_game_position():
        pass
    
    
    def game_over(self, player_turn: str):
        if player_turn == 'b':
            chk_state = 1
        else:
            chk_state = 2

        in_row = 0
        for i in range(max(0, self.prev_i - 5), min(self.BOARD_SIZE - 1, self.prev_i + 5)):
            if self.board[i][self.prev_j] == chk_state:
                in_row += 1
            else:
                in_row = 0
            
            if in_row == 5:
                return True
        in_row = 0
        for j in range(max(0, self.prev_j - 5), min(self.BOARD_SIZE - 1, self.prev_j + 5)):
            if self.board[self.prev_i][j] == chk_state:
                in_row += 1
            else:
                in_row = 0
            
            if in_row == 5:
                return True
            
        in_row = 0
        i = max(0, self.prev_i - 5)
        for j in range(max(0, self.prev_j - 5), min(self.BOARD_SIZE - 1, self.prev_j + 5)):
            if self.board[i][j] == chk_state:
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
            if self.board[i][j] == chk_state:
                in_row += 1
            else:
                in_row = 0
            
            if in_row == 5:
                return True            
            i -= 1
            if i < 0:
                break


        return False
         
            
