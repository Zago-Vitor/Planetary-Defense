import pygame
import random
import math

from config import *
from game.player import Player
from game.enemy import Enemy
from game.bullet import Bullet

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Defesa Planetária")
clock = pygame.time.Clock()

player = Player(WIDTH // 2, HEIGHT // 2)

enemies = []
bullets = []

score = 0
spawn_timer = 0
spawn_delay = 60
difficulty_timer = 0
font = pygame.font.SysFont(None, 36)


def spawn_enemy():
    side = random.randint(0, 3)

    if side == 0:
        x = random.randint(0, WIDTH)
        y = 0
    elif side == 1:
        x = WIDTH
        y = random.randint(0, HEIGHT)
    elif side == 2:
        x = random.randint(0, WIDTH)
        y = HEIGHT
    else:
        x = 0
        y = random.randint(0, HEIGHT)

    enemies.append(Enemy(x, y))


def shoot(mx, my):
    dx = mx - player.x
    dy = my - player.y
    dist = math.sqrt(dx**2 + dy**2)

    speed = 7

    vx = dx / dist * speed
    vy = dy / dist * speed

    bullets.append(Bullet(player.x, player.y, vx, vy))


running = True

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            shoot(mx, my)

    spawn_timer += 1
    difficulty_timer += 1

    if difficulty_timer >= 600:  # a cada 10 segundos
        if spawn_delay > 15:
            spawn_delay -= 5
        difficulty_timer = 0

    if spawn_timer >= spawn_delay:
        spawn_enemy()
        spawn_timer = 0

    for enemy in enemies[:]:
        enemy.move_toward(player.x, player.y)

        dist = math.sqrt(
            (enemy.x - player.x) ** 2 +
            (enemy.y - player.y) ** 2
        )

        if dist < player.radius:
            enemies.remove(enemy)
            player.life -= 1

    for bullet in bullets[:]:
        bullet.move()

        if bullet.x < 0 or bullet.x > WIDTH:
            bullets.remove(bullet)
            continue

        if bullet.y < 0 or bullet.y > HEIGHT:
            bullets.remove(bullet)
            continue

    for bullet in bullets[:]:
        for enemy in enemies[:]:
            dist = math.sqrt(
                (bullet.x - enemy.x) ** 2 +
                (bullet.y - enemy.y) ** 2
            )

            if dist < enemy.radius:
                if bullet in bullets:
                    bullets.remove(bullet)

                if enemy in enemies:
                    enemies.remove(enemy)

                score += 1
                break

    player.draw(screen)

    for enemy in enemies:
        enemy.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)

    text = font.render(
        f"Pontos: {score} Vida: {player.life}",
        True,
        WHITE
    )
    screen.blit(text, (20, 20))

    if player.life <= 0:
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()