import pygame
import pytmx

# Инициализация Pygame
pygame.init()

# Размер окна
WINDOW_SIZE = (800, 600)

# Создание окна
screen = pygame.display.set_mode(WINDOW_SIZE)

# Загрузка карты
tmx_map = pytmx.load_pygame("maps\carta.tmx")

# Функция отрисовки карт
def draw_map():
    for layer in tmx_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_map.get_tile_image_by_gid(gid)
                screen.blit(tile, (x * tmx_map.tilewidth, y * tmx_map.tileheight))


# Главный цикл игры
running = True
while running:
    # Обработка событий Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Отрисовка карты
    draw_map()

    # Обновление экрана
    pygame.display.update()

# Выход из Pygame
pygame.quit()
