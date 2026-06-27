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

game_state = "MENU"


def show_menu():
    title_font = pygame.font.SysFont(None, 72)
    text_font = pygame.font.SysFont(None, 36)

    while True:
        screen.fill(BLACK)

        title = title_font.render("DEFESA PLANETARIA", True, WHITE)
        controls1 = text_font.render("Mouse - Atirar", True, WHITE)
        controls2 = text_font.render("ENTER - Jogar", True, WHITE)
        controls3 = text_font.render("ESC - Sair", True, WHITE)
        objective = text_font.render("Objetivo: Alcance 100 pontos", True, WHITE)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))
        screen.blit(controls1, (WIDTH // 2 - controls1.get_width() // 2, 260))
        screen.blit(controls2, (WIDTH // 2 - controls2.get_width() // 2, 300))
        screen.blit(controls3, (WIDTH // 2 - controls3.get_width() // 2, 340))
        screen.blit(objective, (WIDTH // 2 - objective.get_width() // 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "PLAYING"
                if event.key == pygame.K_ESCAPE:
                    return "QUIT"


def show_victory():
    title_font = pygame.font.SysFont(None, 72)
    text_font = pygame.font.SysFont(None, 36)

    while True:
        screen.fill(BLACK)

        title = title_font.render("VOCE VENCEU!", True, WHITE)
        info1 = text_font.render("R - Jogar novamente", True, WHITE)
        info2 = text_font.render("Fechar janela - Sair", True, WHITE)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 220))
        screen.blit(info1, (WIDTH // 2 - info1.get_width() // 2, 320))
        screen.blit(info2, (WIDTH // 2 - info2.get_width() // 2, 360))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "PLAYING"


def show_game_over():
    title_font = pygame.font.SysFont(None, 72)
    text_font = pygame.font.SysFont(None, 36)

    while True:
        screen.fill(BLACK)

        title = title_font.render("GAME OVER", True, WHITE)
        restart = text_font.render("R - Reiniciar", True, WHITE)
        exit_text = text_font.render("Fechar janela - Sair", True, WHITE)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 220))
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 320))
        screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, 360))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "PLAYING"




def run_game():
    player = Player(WIDTH // 2, HEIGHT // 2)
    enemies = []
    bullets = []

    score = 0
    spawn_timer = 0
    spawn_delay = 60
    difficulty_timer = 0

    font = pygame.font.SysFont(None, 36)

    background = pygame.image.load("/home/zago/PycharmProjects/Planetary-Defense/Assets/Background1.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))



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
        dist = math.sqrt(dx ** 2 + dy ** 2)

        if dist == 0:
            return

        speed = 7
        vx = dx / dist * speed
        vy = dy / dist * speed

        bullets.append(Bullet(player.x, player.y, vx, vy))

    while True:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                shoot(mx, my)

        spawn_timer += 1
        difficulty_timer += 1

        if difficulty_timer >= 600:
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

        hud = font.render(
            f"Pontos: {score} Vida: {player.life}",
            True,
            WHITE
        )
        screen.blit(hud, (20, 20))

        if player.life <= 0:
            return "GAME_OVER"

        if score >= 100:
            return "VICTORY"

        pygame.display.flip()
        clock.tick(FPS)


while True:
    if game_state == "MENU":
        game_state = show_menu()

    elif game_state == "PLAYING":
        game_state = run_game()

    elif game_state == "VICTORY":
        game_state = show_victory()

    elif game_state == "GAME_OVER":
        game_state = show_game_over()

    elif game_state == "QUIT":
        break

pygame.quit()