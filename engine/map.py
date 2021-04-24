import os, pygame
class Map:
    def __init__(self, path, tile_size):
        self.tile_size = tile_size
        map_path = path + "/map.txt"
        config_path = path + "/config.txt"
        self.images = {}

        with open(config_path) as config:
            config = config.read()
            for line in config.split("\n")[:-1]:
                elements = line.split(":")
                self.images[elements[0]] = pygame.image.load(elements[1])

        self.mapdata = []
        with open(map_path) as map:
            map = map.read()
            for line in map.split("\n"):
                line_list = []
                for letter in line:
                    line_list.append(letter)
                self.mapdata.append(line_list)
        self.mapdata = self.mapdata[:-1]
        print(self.mapdata)

    def draw(self, display):

        tile_rects = []
        y = 0
        for row in self.mapdata:
            x = 0
            for tile in row:
                if tile == "0":
                    pass
                else:
                    display.blit(self.images[tile], (x * self.tile_size, y * self.tile_size))
                    tile_rects.append(pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
                x += 1
            x = 0
            y += 1
        return tile_rects
