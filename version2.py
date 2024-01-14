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

    def load_frames(self):
        spritesheet = pygame.image.load("images/sprites/hero/hero_run.png").convert_alpha()
        for i in range(10):
            self.frames.append(spritesheet.subsurface((i * 32, 0, 48, 70)))

    def update(self, keys, tiles, map_width, map_height):
        if keys[pygame.K_LEFT]:
            if self.x - self.speed >= 0:  # Проверяем, не выходит ли игрок за левую границу карты
                self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            if self.x + self.speed <= map_width - self.rect.width:  # Проверяем, не выходит ли игрок за правую границу карты
                self.x += self.speed
        if keys[pygame.K_UP]:
            if self.y - self.speed >= 0:  # Проверяем, не выходит ли игрок за верхнюю границу карты
                self.y -= self.speed
        if keys[pygame.K_DOWN]:
            if self.y + self.speed <= map_height - self.rect.height:  # Проверяем, не выходит ли игрок за нижнюю границу карты
                self.y += self.speed
        #if keys[pygame.K_LEFT]:
        #    self.x -= self.speed
        #if keys[pygame.K_RIGHT]:
        #    self.x += self.speed
        #if keys[pygame.K_UP]:
        #    self.y -= self.speed
        #if keys[pygame.K_DOWN]:
        #    self.y += self.speed

        # Обновляем прямоугольник игрока
        self.rect.center = (self.x, self.y)

        # Проверяем коллизии с тайлами
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                # Обработка коллизии: возвращаем игрока на предыдущую позицию
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


def draw_map(tmx_map):
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
screen = pygame.display.set_mode(screen_size)

tmx_map = pytmx.load_pygame("images/map/map12.tmx")

player = Player(64, 336)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    #player.update(keys, tiles)  # Передаем тайлы для проверки коллизий
    tiles = draw_map(tmx_map)
    player.update(keys, tiles, 1200, 640)
    screen.fill((0, 0, 0))
    tiles.draw(screen)
    screen.blit(player.image, player.rect)
    pygame.display.flip()

pygame.quit()