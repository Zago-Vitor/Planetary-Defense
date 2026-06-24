import pygame
import random
import math

pygame.init()

# Tela
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Defesa Planetária")

# Cores
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 50, 50)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

clock = pygame.time.Clock()

# Planeta
planet_x = WIDTH // 2
planet_y = HEIGHT // 2
planet_radius = 40
planet_life = 5

# Listas
enemies = []
bullets = []

score = 0
running = True