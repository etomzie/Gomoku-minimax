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
        
        return white_score - black_score



    def evaluate_line(self, line, player):
        s = ''.join(line)

        stone = player
        score = 0

        patterns = {
            f"{stone*5}":       10000000,  # Five in a row

            f".{stone*4}.":      100000,   # Open four
            f"{stone*4}.":        10000,   # Closed four
            f".{stone*4}":        10000,

            f".{stone*3}.":        1000,   # Open three
            f"{stone*3}.":          100,   # Closed three
            f".{stone*3}":          100,

            f".{stone*2}.":          50,   # Open two

            # Broken patterns
            f"{stone*2}.{stone*2}": 5000,  # XX_XX
            f"{stone}.{stone*3}":   3000,  # X_XXX
            f"{stone*3}.{stone}":   3000,  # XXX_X

            f"{stone}.{stone*2}":    200,  # X_XX
            f"{stone*2}.{stone}":    200,  # XX_X
        }

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