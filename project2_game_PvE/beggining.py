import pygame
import ctypes
import os
import sys

user32 = ctypes.windll.user32


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Отсутствие файла '{fullname}' привело к фейлу :/")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def button_mouse_pos(x, y):
    if x <= pygame.mouse.get_pos()[0] <= x + 120 and y <= pygame.mouse.get_pos()[1] <= y + 50:
        return True
    return False


def mouse_view():
    if not ((100 < pygame.mouse.get_pos()[0] < w - 100 and 100 < pygame.mouse.get_pos()[1] < h - 100) and
            (h - 200) * 5 // 3 - h + 100 + point <= 0) or status == -1:
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_visible(True)


pygame.init()
size = w, h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
main_screen = pygame.display.set_mode(size)
fon = pygame.transform.scale(load_image('castle.jpg'), (w - 200, (h - 200) * 5 // 3))
help_fon = pygame.transform.scale(load_image('help_fon_demo.jpg'), (w - 200, h - 200))
run = True
status = -1
f1 = True
point = 100
pygame.mouse.set_visible(False)
colors_text = [(255, 255, 255), (0, 0, 0)]
text = pygame.font.Font('freesansbold.ttf', 32).render("press any key", True, (255, 0, 0))
text_new_game = pygame.font.Font('freesansbold.ttf', 16).render("НОВАЯ ИГРА", True, (255, 255, 255))
text_load = pygame.font.Font('freesansbold.ttf', 16).render("ЗАГРУЗИТЬ", True, (255, 255, 255))
text_help = pygame.font.Font('freesansbold.ttf', 16).render("ПОМОЩЬ", True, (255, 255, 255))
text_exit = pygame.font.Font('freesansbold.ttf', 16).render("ВЫХОД", True, (255, 255, 255))
esc_text = pygame.font.Font('freesansbold.ttf', 16).render("НАЗАД", True, (255, 255, 255))
game_name_text = pygame.font.Font('freesansbold.ttf', 64).render("revenge and the dungeon", True, (255, 0, 0))
version_text = pygame.font.Font('freesansbold.ttf', 16).render("version - beta 0.1", True, (255, 255, 255))

while run:
    main_screen.fill((0, 0, 0))
    if status == -1 or status == 0:
        mouse_view()
        main_screen.blit(fon, (100, point))
        main_screen.blit(version_text, (w - 300, h + 200 + point))
        pygame.draw.rect(main_screen, (255, 150, 150), (w // 2 - 120, h // 2 + point + h // 10, 120, 50))
        main_screen.blit(text_new_game, (w // 2 - 115, h // 2 + point + h // 10 + 20))
        pygame.draw.rect(main_screen, (255, 150, 150), (w // 2 - 120, h // 2 + point + 2 * h // 10, 120, 50))
        main_screen.blit(text_load, (w // 2 - 115, h // 2 + point + 2 * h // 10 + 20))
        pygame.draw.rect(main_screen, (255, 150, 150), (w // 2 - 120, h // 2 + point + 3 * h // 10, 120, 50))
        main_screen.blit(text_help, (w // 2 - 115, h // 2 + point + 3 * h // 10 + 20))
        pygame.draw.rect(main_screen, (255, 150, 150), (w // 2 - 120, h // 2 + point + 4 * h // 10, 120, 50))
        main_screen.blit(text_exit, (w // 2 - 115, h // 2 + point + 4 * h // 10 + 20))
        pygame.draw.rect(main_screen, (0, 0, 0), (100, h - 100, w - 200, h - 200))
        pygame.draw.rect(main_screen, (0, 0, 0), (100, 0, w - 200, 100))
        main_screen.blit(game_name_text, (w // 2 - 400, 250 - point))
        if status == -1:
            main_screen.blit(text, (w // 2 - 150, 10))
        if (h - 200) * 5 // 3 - h + 100 + point > 0 and status == 0:
            point -= 1
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                run = False
            if evt.type == pygame.KEYDOWN and status == -1:
                status = 0
            if evt.type == pygame.MOUSEMOTION:
                if button_mouse_pos(w // 2 - 120, h // 2 + point + h // 10):
                    text_new_game = pygame.font.Font('freesansbold.ttf', 16).render("НОВАЯ ИГРА", True, (0, 0, 255))
                elif button_mouse_pos(w // 2 - 120, h // 2 + point + 2 * h // 10):
                    text_load = pygame.font.Font('freesansbold.ttf', 16).render("ЗАГРУЗИТЬ", True, (0, 0, 255))
                elif button_mouse_pos(w // 2 - 120, h // 2 + point + 3 * h // 10):
                    text_help = pygame.font.Font('freesansbold.ttf', 16).render("ПОМОЩЬ", True, (0, 0, 255))
                elif button_mouse_pos(w // 2 - 120, h // 2 + point + 4 * h // 10):
                    text_exit = pygame.font.Font('freesansbold.ttf', 16).render("ВЫХОД", True, (0, 0, 255))
                else:
                    text_new_game = pygame.font.Font('freesansbold.ttf', 16).render("НОВАЯ ИГРА", True, (255, 255, 255))
                    text_load = pygame.font.Font('freesansbold.ttf', 16).render("ЗАГРУЗИТЬ", True, (255, 255, 255))
                    text_help = pygame.font.Font('freesansbold.ttf', 16).render("ПОМОЩЬ", True, (255, 255, 255))
                    text_exit = pygame.font.Font('freesansbold.ttf', 16).render("ВЫХОД", True, (255, 255, 255))
            if evt.type == pygame.MOUSEBUTTONDOWN:
                if button_mouse_pos(w // 2 - 120, h // 2 + point + 4 * h // 10):
                    pygame.quit()
                    exit()
                elif button_mouse_pos(w // 2 - 120, h // 2 + point + 3 * h // 10):
                    status = 3
                elif button_mouse_pos(w // 2 - 120, h // 2 + point + 2 * h // 10):
                    status = 2
    elif status == 3:
        main_screen.blit(help_fon, (100, 100))
        pygame.draw.rect(main_screen, (255, 150, 150), (100, 100, 120, 50))
        main_screen.blit(esc_text, (128, 115))
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                run = False
            if evt.type == pygame.MOUSEBUTTONDOWN and button_mouse_pos(100, 100):
                status = 0
    elif status == 2:
        pygame.draw.rect(main_screen, (128, 128, 128), (100, 100, w - 200, h - 200))
        pygame.draw.rect(main_screen, (255, 150, 150), (100, 100, 120, 50))
        main_screen.blit(esc_text, (128, 115))
        level_text_1 = pygame.font.Font('freesansbold.ttf', 20).render("УРОВЕНЬ 1", True, (255, 255, 255))
        level_text_2 = pygame.font.Font('freesansbold.ttf', 20).render("УРОВЕНЬ 2", True, (255, 255, 255))
        level_text_3 = pygame.font.Font('freesansbold.ttf', 20).render("УРОВЕНЬ 3", True, (255, 255, 255))
        load_text_text = pygame.font.Font('freesansbold.ttf', 20).render("ЗАГРУЗИТЬ", True, (0, 255, 0))
        main_screen.blit(level_text_1, (320, 120))
        main_screen.blit(level_text_2, (320, 320))
        main_screen.blit(level_text_3, (320, 520))
        pygame.draw.rect(main_screen, (255, 150, 150), (440, 110, 130, 40))
        main_screen.blit(load_text_text, (450, 125))
        pygame.draw.rect(main_screen, (255, 150, 150), (440, 310, 130, 40))
        main_screen.blit(load_text_text, (450, 325))
        pygame.draw.rect(main_screen, (255, 150, 150), (440, 510, 130, 40))
        main_screen.blit(load_text_text, (450, 525))
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                run = False
            if evt.type == pygame.MOUSEBUTTONDOWN and button_mouse_pos(100, 100):
                status = 0
    pygame.display.flip()
pygame.quit()
