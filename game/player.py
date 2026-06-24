import pygame
from config import BLUE, PLAYER_RADIUS

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.life = 5
        self.radius = PLAYER_RADIUS

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            BLUE,
            (int(self.x), int(self.y)),
            self.radius
        )