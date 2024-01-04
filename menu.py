import pygame
import pytmx
import sys

pygame.init()
pygame.display.set_caption("Танджиро: в поисках Незуко")

screen_size = width_size, height_size = 1200, 640
screen = pygame.display.set_mode(screen_size)

background = pygame.image.load("images/menu/background.png")

clock = pygame.time.Clock()


# кнопка
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
        screen.fill("white")

        play_mouse_pos = pygame.mouse.get_pos()

        back_play = Button(None, (600, 400), get_font(80), "BACK", "black", "green")

        back_play.change_color(play_mouse_pos)
        back_play.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_play.check_input(play_mouse_pos):
                    main_menu()

        pygame.display.update()


# правила игры
def rules_game():
    while True:
        screen.fill("white")

        rules_mouse_pos = pygame.mouse.get_pos()

        back_rules = Button(None, (600, 400), get_font(80), "BACK", "black",
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


def main_menu():
    while True:
        screen.blit(background, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        text_menu = get_font(100).render("ГЛАВНОЕ МЕНЮ", True, (105,105,105))
        menu_rect = text_menu.get_rect(center=(600, 100))

        # фон кнопки (серый)
        back_image = pygame.image.load("images/menu/button_back.png")

        play_button = Button(back_image, (600, 250), get_font(70), "играть",  (215,252,244),
                             "white")
        rules_button = Button(back_image, (600, 400), get_font(70), "правила",
                              (215,252,244), "white")
        quit_button = Button(back_image, (600, 550), get_font(70), "выйти", (215,252,244),
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


main_menu()
