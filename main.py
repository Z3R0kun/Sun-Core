import pygame, sys
from pygame.locals import *
import engine.animations
import engine.player
import engine.map
pygame.init()

screen_size = (600, 400)
DISPLAY_SIZE = (300, 200)
clock = pygame.time.Clock()

PlayerAnimations = engine.animations.AnimationDatabase()
PlayerAnimations.add_animation("assets/animations/player/idle", [40, 10])
PlayerAnimations.change_animation("idle")
PlayerAnimations.add_animation("assets/animations/player/run", [10, 10])

player = engine.player.Player(50, 50, 16, 16, "assets/animations/player/idle/idle_0.png")
collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

map = engine.map.Map("assets/maps/prototype", 16)
while True:
    clock.tick(60)
    #setting up the display and the screen
    screen = pygame.display.set_mode(screen_size)
    display = pygame.Surface(DISPLAY_SIZE)
    pygame.display.set_caption("A game without a name")
    #we draw on the screen what we need
    display.fill((255, 255, 255))
    tiles = map.draw(display)
    #we check for player movement
    keys = pygame.key.get_pressed()
    player.momentum[0] = 0
    if keys[K_a]:
        player.momentum[0] = -2
        PlayerAnimations.change_animation("run")
    if keys[K_d]:
        player.momentum[0] = 2
        PlayerAnimations.change_animation("run")
    if keys[K_d] and keys[K_a]:
        player.momentum[0] = 0
        PlayerAnimations.change_animation("idle")
    if player.momentum[0] == 0:
        PlayerAnimations.change_animation("idle")


    #we apply gravity to the player
    if not collision_types["bottom"]:
        if player.momentum[1] < 7:
            player.momentum[1] += 1

    #we jump
    if collision_types["bottom"]:
        if keys[K_w]:
            if player.momentum[0] != 0:
                player.momentum[1] = -10
            else:
                player.momentum[1] = - 8



    #we draw the player
    player.texture = PlayerAnimations.get_current_image()
    collision_types = player.move(tiles)
    player.blit(display)

    screen.blit(pygame.transform.scale(display, (screen_size)), (0, 0))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
