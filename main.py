import pygame
import pytmx
import os
import sys


pygame.init()
pygame.display.set_caption("Танджиро: в поисках Незуко")
screen_size = width_size, height_size = 1200, 640
screen = pygame.display.set_mode(screen_size)

background = pygame.image.load("images/menu/background.png")  # фон для меню

map1 = pytmx.load_pygame("images/map/map1.tmx")
map2 = pytmx.load_pygame("images/map/level2.tmx")

class Button:
    # text_color - цвет текста, text_color2 - цвет текста при наведении курсора
    def __init__(self, image, pos, font, text_input, text_color, text_color2):
        self.image = image
        self.pos_x, self.pos_y = pos[0], pos[1]
        self.font = font
        self.text_input = text_input
        self.text_color = text_color
        self.text_color2 = text_color2

        self.text = self.font.render(self.text_input, True, self.text_color)
        if self.image == None:
            self.image = self.text

        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        self.text_rect = self.text.get_rect(center=(self.pos_x, self.pos_y))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    # проверка наведён ли курсор на кнопку
    def check_input(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        else:
            return False

    # изменение цвета при наведении курсора
    def change_color(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.text_color2)
        else:
            self.text = self.font.render(self.text_input, True, self.text_color)


# возвращает шрифт в нужном размере
def get_font(size):
    return pygame.font.Font("images/menu/font.ttf", size)


# играть
def play():
    while True:
        screen.blit(background, (0, 0))
        play_mouse_pos = pygame.mouse.get_pos()

        back_image = pygame.image.load("images/menu/button_back.png")  # фон кнопки (серый)
        level1_button = Button(back_image, (600, 150), get_font(60), "уровень 1", (215, 252, 244),
                             "white")
        level2_button = Button(back_image, (600, 300), get_font(60), "уровень 2", (215, 252, 244),
                             "white")
        level3_button = Button(back_image, (600, 450), get_font(60), "уровень 3", (215, 252, 244),
                             "white")

        back_play = Button(None, (600, 550), get_font(60), "назад", (105, 105, 105),
                           "green")

        for button in[level1_button, level2_button, level3_button, back_play]:
            button.change_color(play_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_play.check_input(play_mouse_pos):
                    main_menu()
                if level1_button.check_input(play_mouse_pos):
                    tiles = draw_map(map1)
                    tiles.draw(screen)
                if level2_button.check_input(play_mouse_pos):
                    pass
                if level3_button.check_input(play_mouse_pos):
                    pass

        pygame.display.update()


# правила игры
def rules_game():
    while True:
        screen.blit(background, (0, 0))

        rules_mouse_pos = pygame.mouse.get_pos()

        back_rules = Button(None, (600, 550), get_font(60), "назад", (105, 105, 105),
                            "green")

        back_rules.change_color(rules_mouse_pos)
        back_rules.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rules.check_input(rules_mouse_pos):
                    main_menu()

        pygame.display.update()

# главное меню
def main_menu():
    while True:
        screen.blit(background, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        text_menu = get_font(100).render("Главное Меню", True, (105, 105, 105))
        menu_rect = text_menu.get_rect(center=(600, 100))

        # фон кнопки (серый)
        back_image = pygame.image.load("images/menu/button_back.png")

        play_button = Button(back_image, (600, 250), get_font(70), "играть",  (215, 252, 244),
                             "white")
        rules_button = Button(back_image, (600, 400), get_font(70), "правила",
                              (215, 252, 244), "white")
        quit_button = Button(back_image, (600, 550), get_font(70), "выйти", (215, 252, 244),
                             "white")

        screen.blit(text_menu, menu_rect)

        for button in [play_button, rules_button, quit_button]:
            button.change_color(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_input(menu_mouse_pos):
                    play()
                if rules_button.check_input(menu_mouse_pos):
                    rules_game()
                if quit_button.check_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


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

    def load_frames(self):
        spritesheet = pygame.image.load("images/sprites/hero/hero_run.png").convert_alpha()
        for i in range(10):
            self.frames.append(spritesheet.subsurface((i * 32, 0, 80, 80)))

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


main_menu()
player = Player(100, 100)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    #tiles = draw_map(map1)

    player.update(keys)

    screen.fill((0, 0, 0))
    #tiles.draw(screen)
    screen.blit(player.image, player.rect)
    pygame.display.flip()

pygame.quit()