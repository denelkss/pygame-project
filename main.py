import pygame
import pytmx
import os


pygame.init()
pygame.display.set_caption("Танджиро: в поисках Незуко")

screen_size = width_size, height_size = 2400, 640
screen = pygame.display.set_mode(screen_size)
tmx_map = pytmx.load_pygame("images\map\map1.tmx")

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


    draw_map()
    pygame.display.update()
pygame.quit()

# 1 уровень - 2400 x 640 (150 х 40 тайлов, 16 х 16 - 1 тайл)