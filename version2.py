import pygame
import pytmx
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = 5
        self.current_frame = 0
        self.frames = []
        self.load_frames()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    # анимация
    def load_frames(self):
        spritesheet = pygame.image.load("images/sprites/hero/hero_run.png").convert_alpha()
        for i in range(10):
            self.frames.append(spritesheet.subsurface((i * 32, 0, 48, 70)))


    # движение и коллизия
    def update(self, keys, tiles, map_width, map_height):
        collision = map1.get_layer_by_name('platforms')
        tiles_collision = []
        for x, y, tile in collision.tiles():
            if (tile):
                tiles_collision.append(pygame.Rect([(x * tile_size), (y * tile_size), tile_size, tile_size]))

        if keys[pygame.K_LEFT]:
            # проверяем, не выходит ли персонаж за левую границу карты
            if (self.x - width_player // 2) - self.speed >= 0:
                self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            # проверяем, не выходит ли персонаж за правую границу карты
            if (self.x + width_player // 2) + self.speed <= map_width:
                self.x += self.speed
        if keys[pygame.K_UP]:
            # проверяем, не выходит ли персонаж за верхнюю границу карты
            if (self.y - height_player // 1) - self.speed >= 0:
                self.y -= self.speed
        if keys[pygame.K_DOWN]:
            # проверяем, не выходит ли персонаж за нижнюю границу карты
            if (self.y + height_player // 2) + self.speed <= map_height:
                self.y += self.speed

        # обновляем прямоугольник персонажа
        self.rect.center = (self.x, self.y)

        # проверяем коллизии персонажа с тайлами
        for tile in tiles_collision:
            if self.rect.colliderect(tile):
                # возвращаем игрока на предыдущую позицию
                if keys[pygame.K_LEFT]:
                    self.x += self.speed
                if keys[pygame.K_RIGHT]:
                    self.x -= self.speed
                if keys[pygame.K_UP]:
                    self.y += self.speed
                if keys[pygame.K_DOWN]:
                    self.y -= self.speed
                self.rect.center = (self.x, self.y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# отрисовка карты
def draw_map(tmx_map):
    collision = tmx_map.get_layer_by_name('platforms')
    tiles = pygame.sprite.Group()
    for layer in tmx_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile_image = tmx_map.get_tile_image_by_gid(gid)
                if tile_image != None:
                    tile = Tile(tile_image, x * tmx_map.tilewidth, y * tmx_map.tileheight)
                    tiles.add(tile)
                    screen.blit(tile_image, (x * tmx_map.tilewidth, y * tmx_map.tileheight))

    return tiles



pygame.init()
pygame.display.set_caption("Танджиро: в поисках Незуко")
screen_size = width_size, height_size = 1200, 640
tile_size = 16
screen = pygame.display.set_mode(screen_size)

map1 = pytmx.load_pygame("images/map/level1.tmx")
map2 = pytmx.load_pygame("images/map/level2.tmx")
map3 = pytmx.load_pygame("images/map/leve3.tmx")

width_player, height_player = 48, 70
player = Player(70, 330)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    tiles = draw_map(map1)

    # обновление игрока
    player.update(keys, tiles, width_size, height_size)

    # отрисовка тайлов и игрока
    screen.fill((0, 0, 0))
    tiles.draw(screen)
    screen.blit(player.image, player.rect)

    pygame.display.flip()

pygame.quit()