import pygame, sys
from pygame.locals import *
import engine.animations
pygame.init()

screen_size = (600, 400)
DISPLAY_SIZE = (300, 200)
clock = pygame.time.Clock()

PlayerAnimations = engine.animations.AnimationDatabase()
PlayerAnimations.add_animation("assets/animations/player/idle", [40, 10])
PlayerAnimations.change_animation("idle")

while True:
    clock.tick(60)
    screen = pygame.display.set_mode(screen_size)
    display = pygame.Surface(DISPLAY_SIZE)
    display.fill((255, 94, 19))

    display.blit(pygame.image.load(PlayerAnimations.get_current_image()), (50, 50))

    screen.blit(pygame.transform.scale(display, (screen_size)), (0, 0))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
