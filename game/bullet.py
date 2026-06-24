import pygame
from config import YELLOW, BULLET_RADIUS

class Bullet:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = BULLET_RADIUS

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            YELLOW,
            (int(self.x), int(self.y)),
            self.radius
        )