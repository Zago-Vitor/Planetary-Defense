import pygame
import math
from config import RED, ENEMY_RADIUS

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = ENEMY_RADIUS
        self.speed = 2

        self.image = pygame.image.load("/home/zago/PycharmProjects/Planetary-Defense/Assets/Meteor.png")
        self.image = pygame.transform.scale(self.image, (40, 40))

    def move_toward(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx**2 + dy**2)

        if dist != 0:
            self.x += dx / dist * self.speed
            self.y += dy / dist * self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x - 20, self.y - 20))

