import pygame
import pytmx
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = 20
        self.current_frame = 0
        self.frames = []
        self.load_frames()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    # Анимация персонажа
    def load_frames(self):
        spritesheet = pygame.image.load("images/sprites/hero/hero_run.png").convert_alpha ()
        for i in range(10):
            self.frames.append(spritesheet.subsurface((i * 32, 0, 80, 80)))

    # Изменение состояния персонажа: перемещение и анмация
    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect.center = (self.x, self.y)


def draw_map(tmx_map):
    for layer in tmx_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_map.get_tile_image_by_gid(gid)
                if tile != None:
                    screen.blit(tile, (x * tmx_map.tilewidth, y * tmx_map.tileheight))


pygame.init()
pygame.display.set_caption("Танджиро: в поисках Незуко")
screen_size = width_size, height_size = 2400, 640
screen = pygame.display.set_mode(screen_size)

tmx_map = pytmx.load_pygame("images/map/map1.tmx")

player = Player(100, 100)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    player.update(keys)

    screen.fill((0, 0, 0))
    draw_map(tmx_map)
    screen.blit(player.image, player.rect)
    pygame.display.flip()

pygame.quit()
