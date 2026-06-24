import pygame
import math
from config import RED, ENEMY_RADIUS

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = ENEMY_RADIUS
        self.speed = 2

    def move_toward(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx**2 + dy**2)

        if dist != 0:
            self.x += dx / dist * self.speed
            self.y += dy / dist * self.speed

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            RED,
            (int(self.x), int(self.y)),
            self.radius
        )