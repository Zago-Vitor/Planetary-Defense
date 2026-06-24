import pygame
import math
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Defesa Planetária")

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Classe da Nave
class Nave:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.radius = 30

    def draw(self):
        # Desenha a nave como um triângulo
        tip_x = self.x + math.cos(math.radians(self.angle)) * 40
        tip_y = self.y + math.sin(math.radians(self.angle)) * 40
        left_x = self.x + math.cos(math.radians(self.angle + 140)) * 20
        left_y = self.y + math.sin(math.radians(self.angle + 140)) * 20
        right_x = self.x + math.cos(math.radians(self.angle - 140)) * 20
        right_y = self.y + math.sin(math.radians(self.angle - 140)) * 20
        pygame.draw.polygon(screen, WHITE, [(tip_x, tip_y), (left_x, left_y), (right_x, right_y)])

    def rotate(self, direction):
        self.angle += direction * 5

# Classe do Tiro
class Tiro:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 10

    def move(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 5)

# Classe do Inimigo
class Inimigo:
    def __init__(self):
        self.x = random.choice([0, WIDTH])
        self.y = random.randint(0, HEIGHT)
        self.speed = 2

    def move(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        self.x += dx / dist * self.speed
        self.y += dy / dist * self.speed

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 10)

# Objetos principais
nave = Nave(WIDTH // 2, HEIGHT // 2)
tiros = []
inimigos = [Inimigo() for _ in range(5)]

# Loop principal
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BLACK)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        nave.rotate(-1)
    if keys[pygame.K_RIGHT]:
        nave.rotate(1)
    if keys[pygame.K_SPACE]:
        tiros.append(Tiro(nave.x, nave.y, nave.angle))

    # Atualiza e desenha tiros
    for tiro in tiros[:]:
        tiro.move()
        tiro.draw()
        if tiro.x < 0 or tiro.x > WIDTH or tiro.y < 0 or tiro.y > HEIGHT:
            tiros.remove(tiro)

    # Atualiza e desenha inimigos
    for inimigo in inimigos:
        inimigo.move(nave.x, nave.y)
        inimigo.draw()

    # Desenha nave
    nave.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
