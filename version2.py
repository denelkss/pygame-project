import pygame
import pytmx
import os
import sys


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

        # действия персонажа (стоять, бежать вправо и влево, прыгать, ранить, смерть)
        self.action = 'stand'
        #self.stand_animation = True
        #self.runR_animation = False
        #self.runL_animation = False
        #self.jump_animation = False
        #self.hit_animation = False
        #self.death_animation = False


        # передвижение
        self.speed = 5
        self.fallspeed = 0
        self.jumpspeed = 10
        self.gravity = 1

        self.stand = pygame.image.load('images/sprites/heroes/tanjiro_stand.png')

        self.run_right = [pygame.image.load('images/sprites/heroes/tanjiro_run1.png'),
                          pygame.image.load('images/sprites/heroes/tanjiro_run2.png'),
                          pygame.image.load('images/sprites/heroes/tanjiro_run3.png'),
                          pygame.image.load('images/sprites/heroes/tanjiro_run4.png'),
                          pygame.image.load('images/sprites/heroes/tanjiro_run5.png')]

        self.run_left = [pygame.image.load('images/sprites/heroes/tanjiro_runL1.png'),
                         pygame.image.load('images/sprites/heroes/tanjiro_runL2.png'),
                         pygame.image.load('images/sprites/heroes/tanjiro_runL3.png'),
                         pygame.image.load('images/sprites/heroes/tanjiro_runL4.png'),
                         pygame.image.load('images/sprites/heroes/tanjiro_runL5.png')]

        self.jump = [pygame.image.load('images/sprites/heroes/tanjiro_jump2.png'),
                     pygame.image.load('images/sprites/heroes/tanjiro_jump3.png')]

        self.hit = [pygame.image.load('images/sprites/heroes/tanjiro_hit1.png'),
                    pygame.image.load('images/sprites/heroes/tanjiro_hit2.png'),
                    pygame.image.load('images/sprites/heroes/tanjiro_hit3.png'),
                    pygame.image.load('images/sprites/heroes/tanjiro_hit4.png')]

        self.death = [pygame.image.load('images/sprites/heroes/tanjiro_death1.png'),
                      pygame.image.load('images/sprites/heroes/tanjiro_death2.png'),
                      pygame.image.load('images/sprites/heroes/tanjiro_death3.png')]

        # анимация
        self.current_frame = 0
        self.image = self.stand

        self.frames = []
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.flip = False

    # обновление анимации
    def animation(self):
        if self.action == 'runR':
            self.current_frame = (self.current_frame + 1) % len(self.run_right)
            self.image = self.run_right[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)

        if self.action == 'runL':
            self.current_frame = (self.current_frame + 1) % len(self.run_left)
            self.image = self.run_left[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)

        if self.action == 'jump':
            self.current_frame = (self.current_frame + 1) % len(self.jump)
            self.image = self.jump[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)

        if self.action == 'stand':
            # анимация
            self.current_frame = 0
            self.image = self.stand

            self.frames = []
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.flip = False

        if self.action == 'death':
            self.current_frame += 1
            if self.current_frame <= 2:
                self.image = self.death[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.center = (self.x, self.y)

    def collide(self, tiles):
        collision = current_map.get_layer_by_name('platforms')
        tiles_collision = []
        for x, y, tile in collision.tiles():
            if (tile):
                tiles_collision.append(pygame.Rect([(x * tile_size), (y * tile_size), tile_size, tile_size]))

        return tiles_collision

    # стоит ли персонаж на земле
    def check_platforms(self):
        collision = current_map.get_layer_by_name('platforms')
        tiles = []
        for x, y, tile in collision.tiles():
            if (tile):
                tiles.append(pygame.Rect([(x * tile_size), (y * tile_size), tile_size, tile_size]))

        check = False
        if (self.rect.collidelistall(tiles)):
            check = True
        return check

    def move(self, tiles, map_width, map_height):
        keys = pygame.key.get_pressed()
        tiles_collision = self.collide(tiles)

        if keys[pygame.K_LEFT] and self.y < 400:
            if self.x - self.speed >= 0:
                self.x -= self.speed

        if keys[pygame.K_RIGHT] and self.y < 350:
            if self.x + self.speed <= map_width:
                self.x += self.speed

        # проверяем коллизии персонажа с тайлами
        for tile in tiles_collision:
            if self.rect.colliderect(tile):
                if keys[pygame.K_LEFT]:
                    if self.x - self.speed >= 0:
                        self.x -= self.speed
                        self.action = 'runL'
                        #self.stand_animation = False
                        #self.runR_animation = False
                        #self.runL_animation = True
                        #self.jump_animation = False

                if keys[pygame.K_RIGHT]:
                    if self.x + self.speed <= map_width:
                        self.x += self.speed
                        self.action = 'runR'
                        #self.stand_animation = False
                        #self.runR_animation = True
                        #self.runL_animation = False
                        #self.jump_animation = False

                if keys[pygame.K_UP] and self.check_platforms():
                    self.y -= self.jumpspeed
                    self.fallspeed = -self.jumpspeed
                    self.action = 'jump'
                    #self.stand_animation = False
                    #self.runR_animation = False
                    #self.runL_animation = False
                    #self.jump_animation = True

                if (not keys[pygame.K_LEFT]) and (not keys[pygame.K_RIGHT]) and (not keys[pygame.K_UP]):
                    self.action = 'stand'
                    #self.stand_animation = True

        if not self.check_platforms():
            self.fallspeed += self.gravity
            self.y += self.fallspeed

        self.rect.center = (self.x, self.y)


class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.pos_x = x
        self.pos_y = y

        self.speed = 3

        self.action = 'runL'

        # self.runL_animation = True  # анимация, когда персонаж направляется в левую сторону
        # self.runR_animation = False  # анимация, когда персонаж направляется в правую сторону

        self.run_left = [pygame.image.load('images/sprites/monsters/pink_monster_runL1.png'),
                         pygame.image.load('images/sprites/monsters/pink_monster_runL2.png'),
                         pygame.image.load('images/sprites/monsters/pink_monster_runL3.png'),
                         pygame.image.load('images/sprites/monsters/pink_monster_runL4.png'),
                         pygame.image.load('images/sprites/monsters/pink_monster_runL5.png'),
                         pygame.image.load('images/sprites/monsters/pink_monster_runL6.png')]

        self.run_right = [pygame.image.load('images/sprites/monsters/pink_monster_runR1.png'),
                          pygame.image.load('images/sprites/monsters/pink_monster_runR2.png'),
                          pygame.image.load('images/sprites/monsters/pink_monster_runR3.png'),
                          pygame.image.load('images/sprites/monsters/pink_monster_runR4.png'),
                          pygame.image.load('images/sprites/monsters/pink_monster_runR5.png'),
                          pygame.image.load('images/sprites/monsters/pink_monster_runR6.png')]

        self.death = [pygame.image.load('images/sprites/monsters/pink_monster_death1.png'),
                      pygame.image.load('images/sprites/monsters/pink_monster_death2.png'),
                      pygame.image.load('images/sprites/monsters/pink_monster_death3.png'),
                      pygame.image.load('images/sprites/monsters/pink_monster_death4.png'),
                      pygame.image.load('images/sprites/monsters/pink_monster_death5.png')]

        self.current_frame = 0
        self.image = self.run_left[0]

        self.frames = []
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def animation(self):
        if self.action == 'runL':
            self.current_frame = (self.current_frame + 1) % len(self.run_left)
            self.image = self.run_left[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)

        if self.action == 'runR':
            self.current_frame = (self.current_frame + 1) % len(self.run_right)
            self.image = self.run_right[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)

        if self.action == 'death':
            self.current_frame += 1
            if self.current_frame <= 4:
                self.image = self.death[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.center = (self.x, self.y)

    def move(self):
        if self.action != 'death':
            if -50 <= self.pos_x - self.x <= 50:
                self.x -= self.speed
                if self.speed > 0:
                    self.action = 'runL'
                else:
                    self.action = 'runR'

            else:
                self.speed = -self.speed
                self.x -= self.speed


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# отрисовка карты
def draw_map(current_map):
    collision = current_map.get_layer_by_name('platforms')
    tiles = pygame.sprite.Group()

    for layer in current_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile_image = current_map.get_tile_image_by_gid(gid)

                if tile_image != None:
                    tile = Tile(tile_image, x * current_map.tilewidth, y * current_map.tileheight)
                    tiles.add(tile)
                    screen.blit(tile_image, (x * current_map.tilewidth, y * current_map.tileheight))

    return tiles


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


# новая текущая карта
def change_map(tmx_map):
    global current_map, player
    current_map = tmx_map

    # координаты игрока (в зависимости от текущей карты)
    if current_map == map1:
        player = Player(70, 340)
    elif current_map == map2:
        player = Player(70, 325)
    elif current_map == map3:
        player = Player(70, 355)


# играть
def play():
    running = True
    while running:
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

        for button in [level1_button, level2_button, level3_button, back_play]:
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
                    change_map(map1)
                    running = False
                if level2_button.check_input(play_mouse_pos):
                    change_map(map2)
                    running = False
                if level3_button.check_input(play_mouse_pos):
                    change_map(map3)
                    running = False

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
    running = True
    while running:
        screen.blit(background, (0, 0))
        menu_mouse_pos = pygame.mouse.get_pos()

        text_menu = get_font(100).render("Главное Меню", True, (105, 105, 105))
        menu_rect = text_menu.get_rect(center=(600, 100))

        # фон кнопки (серый)
        back_image = pygame.image.load("images/menu/button_back.png")

        play_button = Button(back_image, (600, 250), get_font(70), "играть", (215, 252, 244),
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
                    running = False
                if rules_button.check_input(menu_mouse_pos):
                    rules_game()
                if quit_button.check_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


pygame.init()
pygame.display.set_caption("Танджиро: в поисках Незуко")
screen_size = width_size, height_size = 1200, 640
tile_size = 16
screen = pygame.display.set_mode(screen_size)

background = pygame.image.load("images/menu/background.png")  # фон для меню

# зарузка всех карта
map1 = pytmx.load_pygame("images/map/level1.tmx")
map2 = pytmx.load_pygame("images/map/level2.tmx")
map3 = pytmx.load_pygame("images/map/level3.tmx")

current_map = map1  # текущая карта

width_player, height_player = 48, 70
player = Player(70, 330)
monsters_group = pygame.sprite.Group()
pink_monster = Monster(288, 345)
monsters_group.add(pink_monster)

main_menu()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    tiles = draw_map(current_map)

    # обновление игрока
    player.move(tiles, width_size, height_size)
    player.animation()

    pink_monster.move()
    pink_monster.animation()

    if player.rect.collidepoint(pink_monster.rect.midtop):
        pink_monster.action = 'death'
    elif player.rect.collidepoint(pink_monster.rect.midleft) or player.rect.collidepoint(pink_monster.rect.midleft):
        player.action = 'death'

    # отрисовка тайлов и игрока
    screen.fill((0, 0, 0))
    tiles.draw(screen)
    screen.blit(player.image, player.rect)
    screen.blit(pink_monster.image, pink_monster.rect)

    pygame.display.flip()

pygame.quit()
