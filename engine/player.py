import pygame

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


class Player:
    def __init__(self, x, y, w, h, texture, momentum = [0, 0]):
        self.hitbox = pygame.Rect((x, y, w, h))
        self.momentum = momentum
        self.texture = texture
        self.jump_timer = 0

    def blit(self, surface):
        if type(self.texture) == str:
            surface.blit(pygame.image.load(self.texture), (self.hitbox.x, self.hitbox.y))
        else:
            surface.blit(self.texture, (self.hitbox.x, self.hitbox.y))

    def move(self, tiles = []):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.hitbox.x += self.momentum[0]
        hit_list = collision_test(self.hitbox, tiles)
        for tile in hit_list:
            if self.momentum[0] > 0:
                self.hitbox.right = tile.left
                collision_types['right'] = True
            elif self.momentum[0] < 0:
                self.hitbox.left = tile.right
                collision_types['left'] = True
        self.hitbox.y += self.momentum[1]
        hit_list = collision_test(self.hitbox, tiles)
        for tile in hit_list:
            if self.momentum[1] > 0:
                self.hitbox.bottom = tile.top
                collision_types['bottom'] = True
            elif self.momentum[1] < 0:
                self.hitbox.top = tile.bottom
                collision_types['top'] = True
        return collision_types
