import pygame
import pytmx
import os

pygame.init()
pygame.display.set_caption("Танджиро: в поисках Незуко")

screen_size = width_size, height_size = 2400, 640
screen = pygame.display.set_mode(screen_size)
tmx_map = pytmx.load_pygame("images\map\map1.tmx")

tmx_map = pytmx.load_pygame("images/map/map1.tmx")

# Загрузка изображений для анимации персонажа
player_spritesheet = pygame.image.load("images/sprites/hero/hero_run.png").convert_alpha()

# Создание списка спрайтов для анимации персонажа
player_frames = []
for i in range(10):
    player_frames.append(player_spritesheet.subsurface((i * 32, 0, 80, 80)))

# Определение начальной позиции персонажа на карте
player_x = 100
player_y = 100

# Создание спрайта персонажа
player_sprite = pygame.sprite.Sprite()
player_sprite.image = player_frames[0]
player_sprite.rect = player_sprite.image.get_rect()
player_sprite.rect.center = (player_x, player_y)

# Определение скорости перемещения персонажа
player_speed = 20

# Определение текущего кадра анимации персонажа
current_frame = 0

def draw_map():
    for layer in tmx_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_map.get_tile_image_by_gid(gid)
                if tile != None:
                    screen.blit(tile, (x * tmx_map.tilewidth, y * tmx_map.tileheight))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обработка клавиш для перемещения персонажа
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Обновление текущего кадра анимации персонажа
    current_frame += 1
    if current_frame >= len(player_frames):
        current_frame = 0
    player_sprite.image = player_frames[current_frame]

    # Обновление позиции спрайта персонажа на карте
    player_sprite.rect.center = (player_x, player_y)

    # Отрисовка карты и спрайта персонажа на экране
    draw_map()
    screen.blit(player_sprite.image, player_sprite.rect)
    pygame.display.flip()


pygame.quit()
