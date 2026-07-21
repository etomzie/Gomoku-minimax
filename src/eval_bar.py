import pygame

import math

from settings import GameSettings


SCREEN_H = GameSettings.SCREEN_HEIGHT
SCREEN_W = GameSettings.SCREEN_WIDTH

prev = 0

class Eval_Bar():
    def __init__(self):
        self.score = 0 # -10 - 10
    
    
    def score_to_bar(self):
        if self.score >= 10000:
            return 1.0
        if self.score <= -10000:
            return 0.0

        x = self.score / 1000
        return 1 / (1 + math.exp(-x))
    
    def draw(self, screen):
        global prev
        if prev != self.score:
            print(self.score, self.score_to_bar())
            prev = self.score
        scre = self.score_to_bar()
        
        
        pygame.draw.rect(screen, (0, 0, 0), (10, 80, 20, SCREEN_H / 6 * 5))
        
        pygame.draw.rect(screen, (255, 255, 255), (10, 80, 20, (SCREEN_H / 6 * 5) * scre))
        
            
        