import pygame
import pytmx
import os


pygame.init()
pygame.display.set_caption("Танджиро: в поисках Незуко")

WINDOW_SIZE = (2400, 640)
screen = pygame.display.set_mode(WINDOW_SIZE)
tmx_map = pytmx.load_pygame("images\map\map1.tmx")


def load_image(name, colorkey=None):
    fullname = os.path.join('images\sprites', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
#sprite.image = load_image(r"images\sprites\monsters\AnimationSheet_Character.png")
#sprite.rect = sprite.image.get_rect()
#all_sprites.add(sprite)

class AnimatedSprite(pygame.sprite.Sprite):
    sprite.image = load_image("monsters\AnimationSheet_Character.png")
    sprite.rect = sprite.image.get_rect()
    all_sprites.add(sprite)

    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)


    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)  #  f
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

black_ghosts = AnimatedSprite(load_image("monsters\AnimationSheet_Character.png"), 8, 9, 32, 32)


#def draw_map():
#    for layer in tmx_map.visible_layers:
#        if isinstance(layer, pytmx.TiledTileLayer):
#            for x, y, gid in layer:
#                tile = tmx_map.get_tile_image_by_gid(gid)
#                if tile != None:
#                    screen.blit(tile, (x * tmx_map.tilewidth, y * tmx_map.tileheight))

clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(10)

    #draw_map()
    #pygame.display.update()
pygame.quit()