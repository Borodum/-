import pygame
import random
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


def start_screen():
    start_image = load_image('fon.jpg')
    scr1.blit(start_image, (0, 0))
    font = pygame.font.Font(None, 36)
    text = font.render('Нажмите "Esc", чтобы выйти', True, (0, 0, 0))
    w1 = text.get_width()
    scr1.blit(text, (w//2 - w1//2, h - 100))
    pygame.display.flip()
    while True:
        for sth in pygame.event.get():
            if sth.type == pygame.KEYDOWN and sth.key == pygame.K_ESCAPE:
                return


def set_level():
    inp = open('level.txt', 'r')
    field = [i.rstrip('\n') for i in inp.readlines()]
    inp.close()
    box = load_image('box.png')
    grass = load_image('grass.png')
    mar = load_image('mar.png')
    for i in range(w//50):
        for j in range(h//50):
            if field[i][j] == '.' or field[i][j] == '@':
                scr1.blit(grass, (i * 50, j * 50, 50, 50))
            if field[i][j] == 'b':
                scr1.blit(box)


pygame.init()
size = w, h = 700, 393
scr1 = pygame.display.set_mode(size)
f = True
start_screen()
while f:
    scr1.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            f = False
    pygame.display.flip()
pygame.quit()
