import os
import pygame
import ctypes
user32 = ctypes.windll.user32
w, h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


#fon = pygame.transform.scale(load_image('fon.png'), (w - 200, (h - 200) * 3 // 2))
# text = pygame.font.Font('freesansbold.ttf', 32).render("press any key", True, (255, 0, 0))
# text_new_game = pygame.font.Font('freesansbold.ttf', 16).render("НОВАЯ ИГРА", True, (255, 255, 255))
# text_load = pygame.font.Font('freesansbold.ttf', 16).render("ЗАГРУЗИТЬ", True, (255, 255, 255))
# text_help = pygame.font.Font('freesansbold.ttf', 16).render("ПОМОЩЬ", True, (255, 255, 255))
# text_exit = pygame.font.Font('freesansbold.ttf', 16).render("ВЫХОД", True, (255, 255, 255))
#fon = pygame.transform.scale(load_image('fon.png'), (w - 200, (h - 200) * 5 // 3))

def shout(side):
    step = 0
    # if side % 2 == 0:
    #     x1 = x + ghost.rect.size[0]
    #     go_to = 1
    # else:
    #     x1 = x - ghost.rect.size[0]
    #     go_to = -1
    # y1 = y + ghost.rect.size[1] // 2
    for i in range(1, 5000001):
        if i % 1000000 == 0:
            main_screen.blit(hero_shout[side % 2][step], (x, y))
            step += 1
        #if i > 3000000 and (i - 3000000) % 200000 and can_move(block_sprites)[2]:
         #   main_screen.blit(bullet, (x1, y1))
          #  x1 += go_to
        pygame.display.flip()