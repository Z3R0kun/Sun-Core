import pygame, sys, math
from pygame.locals import *
import engine.animations
import engine.map
import engine.pixeltext
import time
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

damage_sound = pygame.mixer.Sound("assets/sounds/sfx/damage.wav")

map = engine.map.Map("assets/maps/prototype", 16)
def read_enemies_map(map_path):
    mapdata = []
    with open(map_path) as map:
        map = map.read()
        for line in map.split("\n"):
            line_list = []
            for letter in line:
                line_list.append(letter)
            mapdata.append(line_list)
    mapdata = mapdata[:-1]
    return mapdata

enemies_map = read_enemies_map("assets/maps/prototype/enemies.txt")


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

#we spawn the enemies
y = 0
sprouts = []
cannons = []
cannon_bullets = []
sprout_bullets = []
for line in enemies_map:
    x = 0
    for block in line:
        if block == "1":
            sprout_animation = engine.animations.AnimationDatabase()
            sprout_animation.add_animation("assets/animations/sprout/idle", [7, 7, 7])
            sprout_animation.change_animation("idle")
            sprout_animation.add_animation("assets/animations/sprout/shoot", [7, 7, 7], loop = False)
            sprouts.append([pygame.Rect((x * 16 + 4, y * 16 + 4, 6, 10)), sprout_animation])
        if block == "2":
            cannon_animation = engine.animations.AnimationDatabase()
            cannon_animation.add_animation("assets/animations/cannon/idle", [40, 7, 7])
            cannon_animation.change_animation("idle")
            timer = 0
            cannons.append([pygame.Rect((x * 16 + 4, y * 16 + 4, 6, 10)), cannon_animation, timer])


        x+= 1
    x = 0
    y += 1

def rect_distance(rect1, rect2):
    x_d = abs(rect1.x - rect2.x)
    y_d = abs(rect1.y - rect2.y)
    d = (x_d**2 + x**2)**0.5
    return d

def death_screen():
    run = True
    font = engine.pixeltext.Font("small")
    bg_color = [255, 255, 255]
    retry_alpha = 0
    quit_alpha = 0
    timer = 0
    while run:

        if bg_color[1] < 10:
            pass
        else:
            bg_color[1] -= 3
            bg_color[2] -= 3

        if timer < 200:
            timer += 1

        if timer > 120:
            if retry_alpha < 254:
                retry_alpha += 1
        if timer > 180:
            if quit_alpha < 254:
                quit_alpha += 1

        screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("YOU DIED!!")
        display = pygame.Surface(DISPLAY_SIZE)
        display.fill(bg_color)
        dead_text = font.generate_text("YOU DIED")
        retry_text = font.generate_text("RETRY")
        quit_text = font.generate_text("QUIT")


        dead_text = pygame.transform.scale(dead_text, (dead_text.get_width() * 2, dead_text.get_height() * 2))
        display.blit(dead_text, (100, 50))
        retry_text = pygame.transform.scale(retry_text, (retry_text.get_width() * 2, retry_text.get_height() * 2))
        retry_rect = retry_text.get_rect()
        retry_rect.x, retry_rect.y = (120, 100)
        retry_text.set_alpha(retry_alpha)
        display.blit(retry_text, (120, 100))
        quit_text = pygame.transform.scale(quit_text, (quit_text.get_width() * 2, quit_text.get_height() * 2))
        quit_rect = quit_text.get_rect()
        quit_rect.x, quit_rect.y = (125, 130)
        quit_text.set_alpha(quit_alpha)
        display.blit(quit_text, (125, 130))



        screen.blit(pygame.transform.scale(display, screen_size), (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                pos = (event.pos[0] /2, event.pos[1] /2)
                if retry_rect.collidepoint(pos):
                    run = False
                if quit_rect.collidepoint(pos):
                    pygame.quit()
                    sys.exit()

while True:
    scroll[0] += (player.x - scroll[0] - 142)/20
    scroll[1] += (player.y - scroll[1] - 108)/20
    clock.tick(60)
    #setting up the display and the screen
    screen = pygame.display.set_mode(screen_size)
    display = pygame.Surface(DISPLAY_SIZE)
    pygame.display.set_caption("Sun Core!")
    #we draw on the screen what we need
    display.fill((255, 255, 255))
    tiles = map.draw(display, scroll)
    for cannon in cannons:
        tiles.append(cannon[0])
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
            player_momentum[1] += 0.3

    #we jump
    if collision_types["bottom"]:
        if keys[K_w]:
            if player_momentum[0] != 0:
                player_momentum[1] = -5
            else:
                player_momentum[1] = - 4


    collision_types = move(player, tiles, player_momentum)


    #we draw the player
    player_texture = PlayerAnimations.get_current_image()
    display.blit(pygame.image.load(player_texture), (player.x - scroll[0], player.y - scroll[1]))

    #we draw the enemies
    for sprout in sprouts:
        sprout[1].change_animation("idle")
        sprout_texture = sprout[1].get_current_image()
        display.blit(pygame.image.load(sprout_texture), (sprout[0].x - scroll[0] - 6, sprout[0].y - scroll[1] - 4))
        if sprout[0].colliderect(player):
            damage_sound.play()
            time.sleep(0.1)
            player.x, player.y = 150, 50
            cannon_bullets = []
            sprout_bullets = []
            death_screen()

    for cannon in cannons:
        loaded = False
        cannon[1].change_animation("idle")
        cannon_texture = cannon[1].get_current_image()
        display.blit(pygame.image.load(cannon_texture), (cannon[0].x - scroll[0] - 6, cannon[0].y - scroll[1] - 4))
        if cannon[2] == 0:
            loaded = True
            cannon[2] = 1
        else:
            cannon[2] += 1
            loaded = False

        if cannon[2] > 100:
            cannon[2] = 0
        if rect_distance(player, cannon[0]) < 140 and loaded:
            cannon_bullet_animation = engine.animations.AnimationDatabase()
            cannon_bullet_animation.add_animation("assets/animations/cannon_bullet/idle", [7, 7])
            cannon_bullet_animation.change_animation("idle")
            life = 0
            if player.x > cannon[0].x:
                side = "right"
            else:
                side = "left"
            cannon_bullets.append([pygame.Rect(cannon[0].x, cannon[0].y, 8, 7), cannon_bullet_animation, life, side])


    for bullet in cannon_bullets:
        if bullet[2] > 300:
            cannon_bullets.remove(bullet)
            continue
        else:
            bullet[2] += 1
        if bullet[3] == "right":
            bullet[0].x += 2
            texture = pygame.image.load(bullet[1].get_current_image())
        else:
            bullet[0].x -= 2
            texture = pygame.transform.flip(pygame.image.load(bullet[1].get_current_image()), True, False)
        display.blit(texture, (bullet[0].x - scroll[0], bullet[0].y - scroll[1]))
        if bullet[0].colliderect(player):
            damage_sound.play()
            time.sleep(0.1)
            player.x, player.y = 150, 50
            cannon_bullets = []
            sprout_bullets = []
            death_screen()

    screen.blit(pygame.transform.scale(display, (screen_size)), (0, 0))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
