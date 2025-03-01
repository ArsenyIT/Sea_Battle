from all_colors import *
import pygame
from pygame.locals import *
pygame.init()

import pygame.mixer
pygame.mixer.init()

pygame.mixer.init()
pygame.mixer.music.load('resours/Сонар.mp3')
pygame.mixer.music.play(-1)

shot_sound = pygame.mixer.Sound('resours/Выстрел Торпеды.mp3')
boom_sound = pygame.mixer.Sound('resours/Взрыв Торпеды.mp3')
win_sound = pygame.mixer.Sound('resours/Победа.mp3')
fail_sound = pygame.mixer.Sound('resours/Поражение.mp3')

size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
Background = DarkCyan
screen.fill(Background)

screen_rect = screen.get_rect()

ship = pygame.Rect(300, 200, 50, 100)
ship.right = screen_rect.right
ship.centery = screen_rect.centery

missile = pygame.Rect(50, 50, 10, 10)
missile.left = screen_rect.left
missile.centery = screen_rect.centery

missile_speed_x = 0
missile_speed_y = 0

ship_speed_y = 1

ship_alive = True
missile_alive = True

missile_launched = False

hp_ship = 10
ammo = 10

FPS = 120
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not missile_launched:
                missile_launched = True
                missile_speed_x = 3
                missile_speed_y = 0
                ammo -= 1
                shot_sound.play()
            elif event.key == pygame.K_w and not missile_launched:
                missile_speed_y = -2
            elif event.key == pygame.K_s and not missile_launched:
                missile_speed_y = 2

    if missile_alive:
        missile.move_ip(missile_speed_x, missile_speed_y)
        if not missile.colliderect(screen_rect):
            missile = pygame.Rect(50, 50, 10, 10)
            missile.left = screen_rect.left
            missile.centery = screen_rect.centery
            pygame.draw.rect(screen, Red, missile)
            missile_speed_x = 0
            missile_launched = False
        if ship_alive and missile.colliderect(ship):
            missile = pygame.Rect(50, 50, 10, 10)
            missile.left = screen_rect.left
            missile.centery = screen_rect.centery
            pygame.draw.rect(screen, Red, missile)
            missile_speed_x = 0
            missile_launched = False
            hp_ship -= 1
            boom_sound.play()
        if ammo == 0 and missile_launched == False:
            missile_alive = False
            missile_launched = True

    if ship_alive:
        ship.move_ip(0, ship_speed_y)
        if ship.bottom > screen_rect.bottom or ship.top < screen_rect.top:
            ship_speed_y = -ship_speed_y
        if hp_ship < 1:
            ship_alive = False

    if hp_ship < 1 and ammo > 0 or hp_ship < 1 and ammo == 0:
        Background = Green
        pygame.mixer.music.stop()
        win_sound.play()

    if ammo < 1 and hp_ship > 0:
        Background = Black
        pygame.mixer.music.stop()
        fail_sound.play()

    screen.fill(Background)
    if ship_alive:
        pygame.draw.rect(screen, Blue, ship)
    if missile_alive:
        pygame.draw.rect(screen, Red, missile)

    text_surface = font.render(f"Торпеды: {ammo}", True, White)
    text_surface2 = font.render(f"Жизни корабля: {hp_ship}", True, White)

    text_rect = text_surface.get_rect()
    text_rect2 = text_surface2.get_rect()
    text_rect.center = (110, 30)
    text_rect2.center = (1100, 30)

    screen.blit(text_surface, text_rect)
    screen.blit(text_surface2, text_rect2)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()