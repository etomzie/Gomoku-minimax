from settings import GameSettings
from Utils.position import Position

B_pat = {
    # Win
    "BBBBB":      1000000,

    # Fours
    ".BBBB.":      100000,

    "BBBB.":        10000,
    ".BBBB":        10000,

    "BBB.B":        10000,
    "BB.BB":        10000,
    "B.BBB":        10000,

    # Threes
    ".BBB.":         3000,

    ".BB.B.":        2000,
    ".B.BB.":        2000,

    "BB.B.":          800,
    ".B.BB":          800,
    "B.B.B":          600,

    # Twos
    ".BB.":           200,

    ".B.B.":          100,
    "BB..":            30,
    "..BB":            30,
}

W_pat = {
    pattern.replace("B", "W"): score
    for pattern, score in B_pat.items()
}
PATTERNS = {}

for pattern, value in W_pat.items():
    PATTERNS[pattern] = value

for pattern, value in B_pat.items():
    PATTERNS[pattern] = -value

PATTERNS_BY_LENGTH = {}

for pattern, value in PATTERNS.items():
    length = len(pattern)

    if length not in PATTERNS_BY_LENGTH:
        PATTERNS_BY_LENGTH[length] = {}

    PATTERNS_BY_LENGTH[length][pattern] = value
    

B_pat_imm = [f"{'B'*5}", f".{'B'*4}."]
W_pat_imm = [f"{'W'*5}", f".{'W'*4}."]

DIRECTIONS = []
CHECK_RADIUS = GameSettings.CHECK_RADIUS
for i in range(CHECK_RADIUS * -1, CHECK_RADIUS + 1):
    for j in range(CHECK_RADIUS * -1, CHECK_RADIUS + 1):
        if i == 0 and j == 0:
            continue
        DIRECTIONS.append((i, j))





class Evaluator():
    def __init__(self):
        self.count = 0


        
    def get_line(self, position, i, j, di, dj):

        line = []

        x, y = i, j
        while 0 <= x-di < 15 and 0 <= y-dj < 15:
            x -= di
            y -= dj

        while 0 <= x < 15 and 0 <= y < 15:
            line.append(position[x][y])
            x += di
            y += dj

        return line
        
    
    

    def static_eval(self, position: Position): # recalculate all lines
        self.count += 1
        score = 0
        
        
        for line in self.get_all_lines(position.position):
            
            # if self.immediate_win(line, 'W'):
            #     return float('inf')

            # if self.immediate_win(line, 'B'):
            #     return float('-inf')


            score += self.evaluate_line(line)

        

        return score

    def immediate_win(self, line, player):
        s = ''.join(line)
        patterns = W_pat_imm if player == 'W' else B_pat_imm
        return any(pattern in s for pattern in patterns)
        


    def evaluate_line(self, line):
        s = ''.join(line)

        score = 0

        for length, patterns in PATTERNS_BY_LENGTH.items():
            for i in range(len(s) - length + 1):
                window = s[i:i+length]

                score += patterns.get(window, 0)

        return score
    
    def get_all_lines(self, position):
        n = 15
        
        # ROWS
        for row in position:
            yield row

        # COLS
        for c in range(n):
            yield [position[r][c] for r in range(n)]

        # DIAGS
        for d in range(-(n - 1), n):
            diag = []

            for r in range(n):
                c = r - d

                if 0 <= c < n:
                    diag.append(position[r][c])

            if len(diag) >= 5:
                yield diag

        for s in range(2 * n - 1):
            diag = []

            for r in range(n):
                c = s - r

                if 0 <= c < n:
                    diag.append(position[r][c])

            if len(diag) >= 5:
                yield diag

    def quick_eval_move(self, pos, move):
        i,j=move

        score=0

        for di,dj in DIRECTIONS:
            ni=i+di
            nj=j+dj

            if 0 <= ni < GameSettings.BOARD_SIZE and 0 <= nj < GameSettings.BOARD_SIZE:
                if pos.position[ni][nj] == 'W':
                    score+=10
                elif pos.position[ni][nj] == 'B':
                    score+=10

        return score