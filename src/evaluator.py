from settings import GameSettings
from Utils.position import Position

B_pat = {
    # Win
    f"{'B'*5}":             1_000_000,

    # Open four
    f".{'B'*4}.":             100_000,

    # Closed four
    f"{'B'*4}.":               10_000,
    f".{'B'*4}":               10_000,

    # Broken fours
    f"{'B'*3}.B":              10_000,
    f"{'B'*2}.{'B'*2}":        10_000,
    f"B.{'B'*3}":              10_000,

    # Open three
    f".{'B'*3}.":               1_000,

    # Broken threes
    f".{'B'*2}.B.":               500,
    f".B.{'B'*2}.":               500,
    f"{'B'*2}.B.":                300,
    f".B.{'B'*2}":                300,
    f"B.B.B":                     300,

    # Open two
    f".{'B'*2}.":                 100,

    # Broken twos
    f".B.B.":                      50,
    f"{'B'*2}..":                  20,
    f"..{'B'*2}":                  20,
}

W_pat = {
    pattern.replace("B", "W"): score
    for pattern, score in B_pat.items()
}

B_pat_imm = [f"{'B'*5}", f".{'B'*4}."]
W_pat_imm = [f"{'W'*5}", f".{'W'*4}."]



class Evaluator():
    def __init__(self):
        pass

    def static_eval(self, position: Position):
        black_score = 0
        white_score = 0
        
        
        
        for line in self.get_all_lines(position.position):
            
            # if self.immediate_win(line, 'W'):
            #     return float('inf')

            # if self.immediate_win(line, 'B'):
            #     return float('-inf')


            black_score += self.evaluate_line(line, "B", position.turn)
            white_score += self.evaluate_line(line, "W", position.turn)
        

        return white_score - black_score

    def immediate_win(self, line, player):
        s = ''.join(line)
        patterns = W_pat_imm if player == 'W' else B_pat_imm
        return any(pattern in s for pattern in patterns)
        


    def evaluate_line(self, line, player, turn):
        s = ''.join(line)


        score = 0
        if player == 'B':
            patterns = B_pat
        else:
            patterns = W_pat



        for pattern, value in patterns.items():
            score += s.count(pattern) * value

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