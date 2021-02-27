import pygame
import ctypes
import os
import sys
import time

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


class Field:
    def __init__(self, side):
        self.size = side

    def load_level(self, file):
        image_grass1 = load_image("grass_path_1.jpg")
        image_stone2 = load_image("stone_block_1.jpg")
        image_enemy_r = load_image("enemy_1_move_right_1.jpg")
        image_enemy_l = load_image("enemy_1_move_left_1.jpg")
        self.image_enemy_r = pygame.transform.scale(image_enemy_r, (self.size, self.size))
        self.image_enemy_l = pygame.transform.scale(image_enemy_l, (self.size, self.size))
        self.image_grass1 = pygame.transform.scale(image_grass1, (self.size, self.size))
        self.stone_image = pygame.transform.scale(image_stone2, (self.size, self.size))
        inp = open(file, 'r')
        new_field = [i.rstrip('\n') for i in inp.readlines()][2:]
        # inp.close()
        for j in range(len(new_field)):
            for i in range(len(new_field[j])):
                self.place = pygame.sprite.Sprite()
                if new_field[j][i] in ['.', 'b', 'E']:
                    self.place.image = self.image_grass1
                    self.place.rect = self.image_grass1.get_rect()
                    self.place.rect.x = i * self.size
                    self.place.rect.y = j * self.size
                    field_sprites.add(self.place)
                if new_field[j][i] == 'b':
                    self.place.image = self.stone_image
                    self.place.rect = self.stone_image.get_rect()
                    self.place.rect.x = i * self.size
                    self.place.rect.y = j * self.size
                    block_sprites.add(self.place)
                    field_sprites.add(self.place)
                if new_field[j][i] == 'E':
                    if i * self.size <= x:
                        self.place.image = self.image_enemy_r
                        self.place.rect = self.image_enemy_r.get_rect()
                    else:
                        self.place.image = self.image_enemy_l
                        self.place.rect = self.image_enemy_l.get_rect()
                    self.place.rect.x = i * self.size
                    self.place.rect.y = j * self.size
                    field_sprites.add(self.place)
                    enemy_sprites.add(self.place)


class Enemy:
    def __init__(self, e_spr):
        self.speed = 1
        self.hp = 1
        self.dmg = 1
        self.enemy = e_spr
        self.time = time.time()

    def check_hero(self):
        if (ghost.rect.x + ghost.rect.w // 2 - self.enemy.rect.x - self.enemy.rect.w // 2) ** 2 + \
                (ghost.rect.y + ghost.rect.h // 2 - self.enemy.rect.y - self.enemy.rect.h // 2) ** 2 < (w // 3) ** 2 \
                and ghost.rect.x != self.enemy.rect.x and ghost.rect.y != self.enemy.rect.y:
            self.enemy.rect.x += (ghost.rect.x - self.enemy.rect.x) // abs(ghost.rect.x - self.enemy.rect.x)
            self.enemy.rect.x += (ghost.rect.y - self.enemy.rect.y) // abs(ghost.rect.y - self.enemy.rect.y)

    def attack(self):
        if self.time - 8 < time.time():
            if (ghost.rect.x + ghost.rect.w // 2 - self.enemy.rect.x - self.enemy.rect.w // 2) ** 2 + \
                    (ghost.rect.y + ghost.rect.h // 2 - self.enemy.rect.y - self.enemy.rect.h // 2) ** 2 < (
                    w // 6) ** 2:
                hero.xp -= self.dmg
                self.time = time.time()
                for i in range(50):
                    pygame.draw.line(main_screen, (255, 0, 0), (ghost.rect.x + ghost.rect.w // 2,
                                                                ghost.rect.y + ghost.rect.h // 2),
                                     (self.enemy.rect.x + self.enemy.rect.w // 2,
                                     self.enemy.rect.y + self.enemy.rect.h // 2), 3)
                    pygame.display.flip()

    def is_dead(self):
        if self.hp <= 0:
            del self


class EvaHero:
    def __init__(self, hero_e, start_pos):
        self.hero = hero_e
        self.xp = 10
        self.xp_max = 10
        self.speed = 1
        self.up_dmg = 0
        self.money = 0
        self.fire = 5
        for srt in field_sprites:
            srt.rect.x += w // 2 - start_pos[0]
            srt.rect.y += h // 2 - start_pos[1]

    def hero_animation(self, turn, step=0):
        return self.hero[turn][step % 8]

    def armour(self):
        pass

    def interface(self):
        pygame.draw.rect(main_screen, (0, 0, 255), (w // 17 * 3, 20, 10 * self.xp_max, 30))
        pygame.draw.rect(main_screen, (255, 0, 0), (w // 17 * 3, 20, 10 * self.xp, 30))
        main_screen.blit(heart, (w // 17 * 3 - 35, 20))
        main_screen.blit(coin, (w // 17 * 5, 10))
        money_text = pygame.font.Font(None, 20).render(f'X {self.money}', True, (255, 255, 255))
        main_screen.blit(money_text, (w // 17 * 5 + 80, 30))
        pygame.draw.rect(main_screen, (255, 150, 150), (0, 0, 120, 50))
        main_screen.blit(esc_text, (28, 15))
        if time.time() - start_time >= hero.fire:
            weapon_r = pygame.font.Font(None, 20).render("READY", True, (0, 255, 0))
        else:
            weapon_r = pygame.font.Font(None, 20) \
                .render(f"RELOADING{'   ->' * int(time.time() - start_time)}", True, (255, 0, 0))
        main_screen.blit(weapon_r, (w // 17 * 8, 20))


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


def shout(side):
    step = 0
    if side % 2 == 0:
        x1 = x + ghost.rect.size[0]
        w1 = ghost.rect.x + ghost.rect.size[0]
        go_to = 1
    else:
        x1 = x - ghost.rect.size[0]
        w1 = ghost.rect.x - ghost.rect.size[0]
        go_to = -1
    y1 = y + ghost.rect.size[1] // 2 - 20
    h1 = ghost.rect.size[1] // 2 - 20 + ghost.rect.y
    for i in range(1, 5000001):
        if i % 1000000 == 0:
            main_screen.blit(hero_shout[side % 2][step], (x, y))
            step += 1
            pygame.display.flip()
        if i > 5000000 - 400:
            main_screen.blit(bullet, (x1, y1))
            x1 += go_to
            w1 += go_to
            for b_spr in enemies_p:
                if (b_spr.enemy.rect.x == w1 - b_spr.enemy.rect.size[0] \
                    or w1 == b_spr.enemy.rect.x + b_spr.enemy.rect.size[0]) \
                        and b_spr.enemy.rect.y < h1 < b_spr.enemy.rect.y + b_spr.enemy.rect.size[1]:
                    field_sprites.remove(b_spr.enemy)
                    enemies.remove(b_spr.enemy)
                    enemies_p.remove(b_spr)
                    b_spr.hp -= 1 + hero.up_dmg
            if i % 100 == 0:
                pygame.display.flip()


def can_move(group):
    x1, y1 = 0, 0
    for b_spr in group:
        if b_spr.rect.x > ghost.rect.x + ghost.rect.size[0] or b_spr.rect.y > ghost.rect.y + ghost.rect.size[1] or \
                ghost.rect.x > b_spr.rect.x + b_spr.rect.size[0] or ghost.rect.y > b_spr.rect.y + b_spr.rect.size[1]:
            pass
        else:
            if b_spr.rect.x == ghost.rect.x + ghost.rect.size[0]:
                x1, y1 = -1, 0
            if ghost.rect.x == b_spr.rect.x + b_spr.rect.size[0]:
                x1, y1 = 1, 0
            if b_spr.rect.y == ghost.rect.y + ghost.rect.size[1]:
                x1, y1 = 0, -1
            if ghost.rect.y == b_spr.rect.y + b_spr.rect.size[1]:
                x1, y1 = 0, 1
            return x1, y1, False
    return 0, 0, True
    # if (x2 > x1 + w1 or y2 > y1 + h1) or (x1 > x2 + w2 or y1 > y2 + h2):


pygame.init()

pygame.mouse.set_visible(False)

size = w, h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
main_screen = pygame.display.set_mode(size)

field_sprites = pygame.sprite.Group()
block_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()

fon = pygame.transform.scale(load_image('castle.jpg'), (w - 200, (h - 200) * 5 // 3))
help_fon = pygame.transform.scale(load_image('help_fon_demo.jpg'), (w - 200, h - 200))
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

x = 1500
y = 1000

run = True
move1 = 1
n = 0
move_side = 2

heart = pygame.transform.scale(load_image('heart.png', -1), (30, 30))
coin = pygame.transform.scale(load_image("coin.jpg", -1), (80, 50))
bullet = pygame.transform.scale(load_image("bullet_1.png", -1), (w // 60, w // 40))
hero_m_r_1 = load_image('gg_move_right1.jpg')
hero_m_r_2 = load_image('gg_move_right2.jpg')
hero_m_r_3 = load_image('gg_move_right3.jpg')
hero_m_r_4 = load_image('gg_move_right4.jpg')
hero_m_r_5 = load_image('gg_move_right5.jpg')
hero_m_r_6 = load_image('gg_move_right6.jpg')
hero_m_r_7 = load_image('gg_move_right7.jpg')
hero_m_r_8 = load_image('gg_move_right8.jpg')
hero_m_l_1 = load_image('gg_move_left1.jpg')
hero_m_l_2 = load_image('gg_move_left2.jpg')
hero_m_l_3 = load_image('gg_move_left3.jpg')
hero_m_l_4 = load_image('gg_move_left4.jpg')
hero_m_l_5 = load_image('gg_move_left5.jpg')
hero_m_l_6 = load_image('gg_move_left6.jpg')
hero_m_l_7 = load_image('gg_move_left7.jpg')
hero_m_l_8 = load_image('gg_move_left8.jpg')
hero_st_r = load_image("gg_stand_right.jpg")
hero_st_l = load_image("gg_stand_left.jpg")
hero_piu_r_1 = load_image("gg_shoot_right1.jpg")
hero_piu_r_2 = load_image("gg_shoot_right2.jpg")
hero_piu_r_3 = load_image("gg_shoot_right3.jpg")
hero_piu_r_4 = load_image("gg_shoot_right4.jpg")
hero_piu_r_5 = load_image("gg_shoot_right5.jpg")
hero_piu_l_1 = load_image("gg_shoot_left1.jpg")
hero_piu_l_2 = load_image("gg_shoot_left2.jpg")
hero_piu_l_3 = load_image("gg_shoot_left3.jpg")
hero_piu_l_4 = load_image("gg_shoot_left4.jpg")
hero_piu_l_5 = load_image("gg_shoot_left5.jpg")

hero_move = [[hero_m_r_1, hero_m_r_2, hero_m_r_3, hero_m_r_4, hero_m_r_5, hero_m_r_6, hero_m_r_7, hero_m_r_8],
             [hero_m_l_1, hero_m_l_2, hero_m_l_3, hero_m_l_4, hero_m_l_5, hero_m_l_6, hero_m_l_7, hero_m_l_8],
             [hero_st_r], [hero_st_l]]
hero_shout = [[hero_piu_r_1, hero_piu_r_2, hero_piu_r_3, hero_piu_r_4, hero_piu_r_5],
              [hero_piu_l_1, hero_piu_l_2, hero_piu_l_3, hero_piu_l_4, hero_piu_l_5]]
field = Field(w // 20)
field.load_level("level1")
w1, h1 = 0, 0
hero = EvaHero(hero_move, (x, y))
ghost = pygame.sprite.Sprite()
ghost.rect = pygame.Surface(hero_m_r_1.get_size()).get_rect()
enemies = list()
enemies_p = list()
for spr in enemy_sprites:
    enm = Enemy(spr)
    enemies_p.append(enm)
    enemies.append(enm.enemy)
x, y = w // 2, h // 2
start_time = time.time() - hero.fire
while run:
    mouse_view()
    main_screen.fill((0, 0, 0))
    if status == 1:
        if time.time() - start_time > hero.fire:
            start_time = time.time() - hero.fire
        ghost.rect.x = x
        ghost.rect.y = y
        main_screen.fill((0, 0, 0))
        field_sprites.draw(main_screen)

        if move1 % 10 == 0:
            n += 1

        if move_side > 1:
            main_screen.blit(hero.hero_animation(move_side), (x, y))
        else:
            main_screen.blit(hero.hero_animation(move_side, n), (x, y))

        pygame.draw.rect(main_screen, (0, 0, 0), (0, 0, w, 100))
        pygame.draw.rect(main_screen, (0, 0, 0), (0, 0, 100, h))
        pygame.draw.rect(main_screen, (0, 0, 0), (w - 100, 0, 100, h))
        pygame.draw.rect(main_screen, (0, 0, 0), (0, h - 100, w, 100))

        hero.interface()

        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                run = False

            if evt.type == pygame.KEYUP and (evt.key == pygame.K_d or evt.key == pygame.K_s or evt.key == pygame.K_w):
                move_side = 2
            elif evt.type == pygame.KEYUP and evt.key == pygame.K_a:
                move_side = 3

            if evt.type == pygame.KEYDOWN and evt.key == pygame.K_SPACE and time.time() - start_time >= hero.fire:
                shout(move_side)
                start_time += hero.fire

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_s] or keys[pygame.K_w]:
            move1 += 1

        cort = can_move(block_sprites)
        if cort[2]:

            if keys[pygame.K_a]:
                move_side = 1
                if (x > w // 2 or list(field_sprites)[0].rect.x >= 100) and x >= list(field_sprites)[0].rect.x:
                    x -= 1
                elif x >= list(field_sprites)[0].rect.x:
                    for spr in field_sprites:
                        spr.rect.x += 1

            if keys[pygame.K_d]:
                move_side = 0
                if x > w // 2 and list(field_sprites)[-1].rect.x > w - 100:
                    for spr in field_sprites:
                        spr.rect.x -= 1
                elif x < w - 100 - hero.hero_animation(move_side, n).get_size()[0]:
                    x += 1

            if keys[pygame.K_s]:
                if move_side == 3:
                    move_side = 1
                if move_side == 2:
                    move_side = 0
                if y > h // 2 and list(field_sprites)[-1].rect.y > h - 100:
                    for spr in field_sprites:
                        spr.rect.y -= 1
                elif y < h - 100 - hero.hero_animation(move_side, n).get_size()[1]:
                    y += 1

            if keys[pygame.K_w]:
                if move_side == 3:
                    move_side = 1
                if move_side == 2:
                    move_side = 0
                if (y > h // 2 or list(field_sprites)[0].rect.y >= 100) and y >= list(field_sprites)[0].rect.y:
                    y -= 1
                elif y >= list(field_sprites)[0].rect.y:
                    for spr in field_sprites:
                        spr.rect.y += 1

        for e in enemies_p:
            e.check_hero()
            e.attack()
            e.is_dead()
        x += cort[0]
        y += cort[1]
        if hero.xp == 0 or len(enemies_p) == 0:
            if hero.xp == 0:
                death_text = pygame.font.Font('freesansbold.ttf', 64).render("ВЫ УМЕРЛИ", True, (255, 0, 0))
            else:
                death_text = pygame.font.Font('freesansbold.ttf', 64).render("ПОБЕДА", True, (0, 255, 0))
            for i in range(400):
                pygame.draw.rect(main_screen, (0, 0, 0), (0, 0, w, h))
                main_screen.blit(death_text, (w // 2 - 200, h // 2 - 20))
                pygame.display.flip()
            status = 0
    elif status == -1 or status == 0:
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
                elif button_mouse_pos(w // 2 - 120, h // 2 + point + h // 10):
                    surf = pygame.transform.scale(load_image("begin.png"), (w - 200, h - 200))
                    text = pygame.font.Font('freesansbold.ttf', 32).render("press any key", True, (255, 0, 0))
                    roof = 0
                    while int(roof) < h:
                        main_screen.blit(surf, (100, 100))
                        pygame.draw.rect(main_screen, (0, 0, 0), (100, roof, w - 200, h - 100))
                        roof += 0.2
                        pygame.display.flip()
                    status = 1

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
