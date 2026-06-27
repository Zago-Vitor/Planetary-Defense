import pygame
from config import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.life = 5
        self.radius = 40

        self.image = pygame.image.load("/home/zago/PycharmProjects/Planetary-Defense/Assets/Ship1.png")
        self.image = pygame.transform.scale(self.image, (80, 80))

    def draw(self, screen):
        screen.blit(self.image, (self.x - 40, self.y - 40))