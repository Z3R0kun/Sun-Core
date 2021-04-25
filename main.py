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
player = pygame.Rect((150, 50, 16, 16))
collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

map = engine.map.Map("assets/maps/prototype", 16)

scroll = [0, 0]

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, tiles = [], momentum = []):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += momentum[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if momentum[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif momentum[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += momentum[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if momentum[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif momentum[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return collision_types

player_momentum = [0, 0]
collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
while True:
    scroll[0] += (player.x - scroll[0] - 142)/20
    scroll[1] += (player.y - scroll[1] - 108)/20
    clock.tick(60)
    #setting up the display and the screen
    screen = pygame.display.set_mode(screen_size)
    display = pygame.Surface(DISPLAY_SIZE)
    pygame.display.set_caption("A game without a name")
    #we draw on the screen what we need
    display.fill((255, 255, 255))
    tiles = map.draw(display, scroll)
    #we check for player movement
    keys = pygame.key.get_pressed()
    player_momentum[0] = 0
    if keys[K_a]:
        player_momentum[0] = -2
        PlayerAnimations.change_animation("run")
    if keys[K_d]:
        player_momentum[0] = 2
        PlayerAnimations.change_animation("run")
    if keys[K_d] and keys[K_a]:
        player_momentum[0] = 0
        PlayerAnimations.change_animation("idle")
    if player_momentum[0] == 0:
        PlayerAnimations.change_animation("idle")


    #we apply gravity to the player
    if not collision_types["bottom"]:
        if player_momentum[1] < 7:
            player_momentum[1] += 1

    #we jump
    if collision_types["bottom"]:
        if keys[K_w]:
            if player_momentum[0] != 0:
                player_momentum[1] = -10
            else:
                player_momentum[1] = - 8


    collision_types = move(player, tiles, player_momentum)
    #we draw the player
    player_texture = PlayerAnimations.get_current_image()
    display.blit(pygame.image.load(player_texture), (player.x - scroll[0], player.y - scroll[1]))


    screen.blit(pygame.transform.scale(display, (screen_size)), (0, 0))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
