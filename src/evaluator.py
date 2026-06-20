from settings import GameSettings
from Utils.position import Position

class Evaluator():
    def __init__(self):
        pass

    def static_eval(self, position: Position):
        black_score = 0
        white_score = 0

        for line in self.get_all_lines(position.position):
            black_score += self.evaluate_line(line, "B")
            white_score += self.evaluate_line(line, "W")



    def evaluate_line(self, line, player):
        s = ''.join(line)

        if player == "B":
            stone = "B"
        else:
            stone = "W"

        score = 0

        score += s.count(f".{stone*4}.") * 100000
        score += s.count(f".{stone*3}.") * 1000

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