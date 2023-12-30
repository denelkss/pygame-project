import pygame
import pytmx
import os
from csv import reader


pygame.init()
pygame.display.set_caption("Танджиро: в поисках Незуко")

screen_size = width_size, height_size = 1200, 640
screen = pygame.display.set_mode(screen_size)
tile_size = 16  # размер одного тайла
clock = pygame.time.Clock()
map1 = pytmx.load_pygame("images/map/map1.tmx")

# информация о 1 уровне
level1 = {'other': 'images/map/map1/map1_other.csv',
          'earth 2': 'images/map/map1/map1_earth 2.csv',
          'earth': 'images/map/map1/map1_earth.csv',
          'rocks': 'images/map/map1/map1_rocks.csv',
          'sea': 'images/map/map1/map1_sea.csv',
          'clouds': 'images/map/map1/map1_clouds.csv',
          'sky': 'images/map/map1/map1_sky.csv'}



# функция для импорта csv файлов
def csv_layout(path):
    with open(path) as map:
        earth_map = []
        level = reader(map, delimiter=',')
        for row in level:
            earth_map.append(list(row))
        return earth_map

# функция для создания тайлов из png картинки
def cut_tileset(path):
    surface = pygame.image.load(path).convert_alpha()

    # количество тайлов (в длину и высоту)
    tile_count_x = surface.get_size()[0] // tile_size
    tile_count_y = surface.get_size()[1] // tile_size

    cut_tiles = []  # вырезанные тайлы
    for row in range(tile_count_y):
        for col in range(tile_count_x):
            x = col * tile_size
            y = row * tile_size
            new_surface = pygame.Surface((tile_size, tile_size))
            new_surface.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surface)

    return cut_tiles

class Tile(pygame.sprite.Sprite):
	def __init__(self, size, x, y):
		super().__init__()
		self.image = pygame.Surface((size, size))
		self.rect = self.image.get_rect(topleft = (x,y))

	def update(self,shift):
		self.rect.x += shift

class StaticTile(Tile):
	def __init__(self, size, x, y, surface):
		super().__init__(size, x, y)
		self.image = surface

# класс уровня
class Level:
    def __init__(self, data_level, surface):
        self.display_surface = surface

        earth_layout = csv_layout(level1['earth'])
        self.earth_sprites = self.create_tileset(earth_layout, 'earth')

    def create_tileset(self, layoyt, name_tile):
        sprite_group = pygame.sprite.Group()

        for index_row, row in enumerate(layoyt):
            for index_col, value in enumerate(row):  # найти индекс и значение x
                if value != '-1':  # -1, если пусто
                    x = index_col * tile_size
                    y = index_row * tile_size

                    if name_tile == 'earth':
                        earth_tile = cut_tileset('images/map/tilesets_png/tileset1.png')
                        tile_surface = earth_tile[int(value)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    sprite_group.add(sprite)

        return sprite_group

    def run(self):
        self.earth_sprites.draw(self.display_surface)


level = Level(level1, screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('black')
    level.run()

    pygame.display.update()
    clock.tick(60)
pygame.quit()

# 1 уровень - 2400 x 640 (150 х 40 тайлов, 16 х 16 - 1 тайл)