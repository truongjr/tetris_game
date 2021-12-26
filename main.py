import sys
import time

import pygame as pg
import random

s_width = 800
s_height = 700
p_width = 300
p_height = 600
X = (s_width - p_width) // 2
Y = s_height - p_height

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 51, 51)
LGRAY = (230, 230, 250)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
LBLUE = (30, 144, 255)
list_text = ['score', 'level', 'line']

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shape = [S, Z, I, O, J, L, T]

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((s_width, s_height))
pg.display.set_caption('T E T I S')
op_list = [pg.image.load('level/easy1.png'), pg.image.load('level/medium1.png'), pg.image.load('level/hard1.png')]
lv = [pg.image.load('level/easy.png'), pg.image.load('level/medium.png'), pg.image.load('level/hard.png')]


def check_pos_in_circle(cir_pos, mouse_pos):
    return (mouse_pos[0] - cir_pos[0]) ** 2 + (mouse_pos[1] - cir_pos[1]) ** 2 <= cir_pos[2] ** 2

class ToggleButton:

    def __init__(self, x, y, w, h, choose, toggle_list, pos_option_list, pos_toggle):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.circle_pos = (x + 50, y + 50, 50)
        self.toggle_list = toggle_list
        self.choose = choose
        self.rect = pg.Rect(self.x - 10, self.y + self.choose.get_height() - 20, 180 + 30, 160)
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1
        self.pos_clicked = (x + 50, y + 50)
        self.pos_clicked_temp = (0, 0)
        self.pos_option_list = pos_option_list
        self.pos_toggle = pos_toggle
        self.on = pg.image.load('on.png')
        self.off = pg.image.load('off.png')
        self.adj = [True for i in range(len(self.toggle_list))]

    def draw(self, surface):
        surface.blit(self.choose, (self.x, self.y))
        if self.draw_menu:
            surface.blit(pg.transform.scale(pg.image.load('level/bg.png'), (180 + 30, 160)),
                         (self.x, self.y + self.choose.get_height() - 20))
            for i in range(len(self.toggle_list)):
                text = pg.font.Font('pridib.ttf', 20).render(self.toggle_list[i] + ' : : ', True, (0, 0, 0))
                surface.blit(text, self.pos_option_list[i])
                if self.adj[i]:
                    surface.blit(self.on, self.pos_toggle[i])
                else:
                    surface.blit(self.off, self.pos_toggle[i])

    def update(self, list_event):
        mouse_pos = pg.mouse.get_pos()
        self.menu_active = check_pos_in_circle(self.circle_pos, mouse_pos)
        self.active_option = -1
        if self.rect.collidepoint(mouse_pos):
            self.menu_active = True if check_pos_in_circle((self.x + 50, self.y + 50, 50) or (
                        check_pos_in_circle((self.circle_pos[0], self.circle_pos[1], 50),
                                            self.pos_clicked_temp) or self.rect.collidepoint(self.pos_clicked)),
                                                           self.pos_clicked) else False
            for i in range(len(self.toggle_list)):
                temp = pg.Rect(self.pos_toggle[i] + (50, 50))
                if temp.collidepoint(mouse_pos):
                    self.active_option = i

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event_item in list_event:
            if event_item.type == pg.MOUSEBUTTONDOWN:
                if self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    self.adj[self.active_option] = not self.adj[self.active_option]
                    return self.adj
                elif self.menu_active:
                    self.draw_menu = not self.draw_menu
            if event_item.type == pg.MOUSEBUTTONUP:
                self.pos_clicked_temp = self.pos_clicked
                self.pos_clicked = pg.mouse.get_pos()

        return self.adj


class OptionBox:

    def __init__(self, x, y, w, h, choose, list_level, option_list, pos_option_list = (), selected=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.circle_pos = (x + 50, y + 50, 50)
        self.level_list = list_level
        self.option_list = option_list
        self.selected = selected
        self.choose = choose
        self.rect = pg.Rect(self.x - 10, self.y + self.choose.get_height() - 20, 180 + len(self.option_list) * 80, 160)
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1
        self.pos_clicked = (x + 50, y + 50)
        self.pos_option_list = pos_option_list

    def draw(self, surface):
        surface.blit(self.choose, (self.x, self.y))
        if self.draw_menu:
            surface.blit(pg.transform.scale(pg.image.load('level/bg.png'), (180 + len(self.option_list) * 80, 160)),
                         (self.x, self.y + self.choose.get_height() - 20))
            for i, value in enumerate(self.option_list, 0):
                surface.blit(value, (self.pos_option_list[i]))
                # print(self.x + self.space + i * 80 + self.space * i, self.y + 120)

    def update(self, list_event):
        mouse_pos = pg.mouse.get_pos()
        self.menu_active = check_pos_in_circle(self.circle_pos, mouse_pos)
        self.active_option = -1
        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.menu_active = True if check_pos_in_circle((self.x + 50, self.y + 50, 50), self.pos_clicked) else False
            for i in range(len(self.option_list)):
                if check_pos_in_circle((self.pos_option_list[i][0] + 40, self.pos_option_list[i][1] + 40, 40),
                                       mouse_pos):
                    self.active_option = i
                    break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event_item in list_event:
            if event_item.type == pg.MOUSEBUTTONDOWN:
                if self.draw_menu and self.active_option >= 0:
                    self.selected = self.active_option
                    self.draw_menu = False
                    self.choose = self.level_list[self.active_option]
                    # print(self.active_option)
                    return self.active_option
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
            if event_item.type == pg.MOUSEBUTTONUP:
                self.pos_clicked = pg.mouse.get_pos()

        return -1


def draw_grid():
    pg.draw.rect(screen, LGRAY, ((s_width - p_width) // 2, s_height - p_height, p_width, p_height))
    pg.draw.rect(screen, BLACK, ((s_width - p_width) // 2, s_height - p_height, p_width, p_height - 1), 2)
    for i in range(0, p_width, 30):
        pg.draw.line(screen, BLACK, (i + (s_width - p_width) // 2, s_height - p_height),
                     (i + (s_width - p_width) // 2, s_height), 1)
    for i in range(0, p_height, 30):
        pg.draw.line(screen, BLACK, ((s_width - p_width) // 2, s_height - p_height + i),
                     (p_width + (s_width - p_width) // 2, s_height - p_height + i), 1)


def draw_start_menu(surface):
    pg.draw.rect(surface, WHITE, (0, 0, s_width, s_height))
    font = pg.font.SysFont('comicsans', 130)
    label = font.render('T E T R I S', True, BLACK)
    surface.blit(label, ((s_width - label.get_width()) // 2, 30))
    Ox = s_width // 2
    Oy = s_height // 2 - 100
    play_button = pg.image.load('play.png')
    setting_button = pg.image.load('setting.png')
    ranking_button = pg.image.load('rank/ranking.png')
    level_button = pg.image.load('level/level.png')
    info_button = pg.image.load('information.png')
    button = [setting_button, level_button, ranking_button, info_button]
    surface.blit(play_button, ((s_width - play_button.get_width()) // 2, 230))
    for i in range(4):
        surface.blit(button[i], (80 * (i + 1) + i * 100, 450))
        # print((80 * (i + 1) + i * 100, 450))


def draw_rank(surface, score_list):
    pg.draw.rect(surface, WHITE, (0, 0, s_width, s_height))
    rank = pg.image.load('rank/ranking.png')
    rank_title = pg.font.Font('pridib.ttf', 50).render('Bảng xếp hạng', True, BLACK)
    surface_title = pg.Surface((rank.get_width() + rank_title.get_width() + 20, rank.get_height()))
    surface_title.fill(WHITE)
    surface_title.blit(rank, (0, 0))
    surface_title.blit(rank_title, (rank.get_width() + 10, surface_title.get_height() - rank_title.get_height()))
    surface.blit(surface_title, ((s_width - surface_title.get_width()) // 2, 30))

    surface_list = pg.Surface((rank.get_width() + rank_title.get_width() + 20, 500))
    surface_list.fill(WHITE)
    h_format = 70
    for i in range(5):
        rank_item = pg.image.load('rank/number-' + str(i + 1) + '.png')
        score = pg.font.Font('pridib.ttf', 40).render(str(score_list[i]), True, BLACK)
        surface_list.blit(rank_item, (0, h_format * i + 20 * i))
        surface_list.blit(score, (
            rank_item.get_width() + 20, rank_item.get_height() // 2 + h_format * i - score.get_height() // 2 + 20 * i))
        # print(rank_item.get_width() + 10 + score.get_width())
        # print(rank)

    surface.blit(surface_list, ((surface.get_width() - surface_list.get_width()) // 2, 200))


def draw_level(surface):
    pg.draw.rect(surface, WHITE, (0, 0, s_width, s_height))
    menu = pg.image.load('level/levelbg.png')
    choose = pg.image.load('level/choose.png')
    easy_text = pg.font.Font('pacifico.ttf', 30).render('dễ', True, BLACK)
    medium_text = pg.font.Font('pacifico.ttf', 30).render('trung bình', True, BLACK)
    hard_text = pg.font.Font('pacifico.ttf', 30).render('khó', True, BLACK)
    choose_level = pg.font.Font('pacifico.ttf', 30).render('chọn', True, BLACK)
    surface_menu = pg.Surface((menu.get_width(), menu.get_height() + choose.get_height() // 2))
    surface_menu.fill(WHITE)
    surface_menu.blit(choose, ((surface_menu.get_width() - choose.get_width()) // 2, -50))
    surface_menu.blit(menu, (0, 15))
    # surface_menu.blit(level1, (0, 0))
    surface.blit(surface_menu,
                 ((surface.get_width() - menu.get_width()) // 2, (surface.get_height() - menu.get_height()) // 2))


def draw_information_game(surface):
    pg.draw.rect(surface, WHITE, (0, 0, s_width, s_height))
    ptit_logo = pg.image.load('ptitlogo.png')
    # surface.blit(ptit_logo, (10, 10))
    name_vi = pg.font.Font('pridib.ttf', 25).render('Học viện Công Nghệ Bưu Chính Viễn Thông'.upper(), True, BLACK)
    name_en = pg.font.Font('pridil.ttf', 20).render('Posts and Telecommunications Institute of Technology', True, RED)
    name_project = pg.font.Font('pridil.ttf', 30).render('Đồ án :', True, BLACK)
    name_game = pg.font.Font('monoton.ttf', 80).render('GAME  TETRIS', True, BLACK)
    name_teacher = pg.font.Font('pridib.ttf', 20).render('Giảng viên hướng dẫn :', True, BLACK)
    name_info_teacher = pg.font.Font('pridil.ttf', 20).render('TS. Nguyễn Thị Tuyết Hải', True, BLACK)
    name_student = pg.font.Font('pridib.ttf', 20).render('Sinh viên thực hiện :', True, BLACK)
    name_info_student1 = pg.font.Font('pridil.ttf', 20).render('Nguyễn Hữu Trưởng - N19DCCN221', True, BLACK)
    name_info_student2 = pg.font.Font('pridil.ttf', 20).render('Nguyễn Nhật Thanh - N19DCCN190', True, BLACK)
    day_info = pg.font.Font('pridil.ttf', 20).render('TP Hồ Chí Minh Ngày 24 Tháng 12 Năm 2021', True, BLACK)
    # surface.blit(font, (10 + ptit_logo.get_width(), 10 + ptit_logo.get_height() // 2))
    surface_ptit = pg.Surface((ptit_logo.get_width() + name_vi.get_width() + 20, ptit_logo.get_height()))
    surface_infor = pg.Surface((max(name_game.get_width() + 20,
                                    name_teacher.get_width() + name_info_teacher.get_width() + 20),
                                name_game.get_height() * 5 + name_project.get_height() + name_game.get_height() + 30))
    x_format = (surface_infor.get_width() - name_teacher.get_width() - name_info_student1.get_width()) // 2
    y_format = (
                       surface_infor.get_width() - name_teacher.get_width() - name_info_student1.get_width()) // 2 + name_teacher.get_width() + 10
    h_format = 0
    surface_infor.fill(WHITE)
    surface_infor.blit(name_project, ((surface_infor.get_width() - name_project.get_width()) // 2, h_format))
    h_format += name_project.get_height()
    surface_infor.blit(name_game, ((surface_infor.get_width() - name_game.get_width()) // 2, h_format))
    h_format += name_game.get_height() + 50
    surface_infor.blit(name_teacher, (x_format, h_format))
    surface_infor.blit(name_info_teacher, (y_format, h_format))
    h_format += name_info_teacher.get_height()
    surface_infor.blit(name_student, (x_format, h_format))
    surface_infor.blit(name_info_student1, (y_format, h_format))
    h_format += name_info_student1.get_height()
    surface_infor.blit(name_info_student2, (y_format, h_format))
    h_format += 150
    surface_infor.blit(day_info, ((surface_infor.get_width() - day_info.get_width()) // 2, h_format))

    surface_ptit.fill(WHITE)
    surface_ptit.blit(ptit_logo, (0, 0))
    surface_ptit.blit(name_vi, (ptit_logo.get_width() + 10, ptit_logo.get_height() // 2 - name_vi.get_height()))
    surface_ptit.blit(name_en, (ptit_logo.get_width() + 10, ptit_logo.get_height() // 2))
    surface.blit(surface_ptit, ((s_width - surface_ptit.get_width()) // 2, 30))

    surface.blit(surface_infor, ((surface.get_width() - surface_infor.get_width()) // 2, 200))


def draw_info():
    # pg.draw.rect()
    text_surface = pg.font.SysFont('comicsans', 20, bold=True)
    # DISPLAYSURF.blit(text_surface, )
    pg.draw.rect(screen, YELLOW, (30, Y, 190, 300), 0, 10, 10, 10, 10)
    pg.draw.rect(screen, YELLOW, (X + 300 + 30, Y, 190, 300), 0, 10, 10, 10, 10)
    for i in range(7):
        if i % 2 == 0:
            # print(Y + 42 * i + 10)
            continue
        pg.draw.rect(screen, BLACK, (50, Y + 42 * i, 150, 48), True, 10, 10, 10, 10)
    for i in range(3):
        label = text_surface.render(list_text[i], True, BLACK)
        screen.blit(label, (60, Y + 84 * i + 10))
        # print(Y + 84 * i + 10)

    label = text_surface.render('next block', True, BLACK)
    screen.blit(label, (X + 300 + 60, 110))


if __name__ == '__main__':
    x = 0
    yes_level = False
    yes_setting = False
    rank_list = [122333, 1232341, 5432344, 5623453, 3654234234]
    rank_list.sort(reverse=True)
    level_list = OptionBox(260, 450, 100, 100, pg.image.load('level/level.png'), lv,
                      (pg.image.load('level/easy1.png'), pg.image.load('level/medium1.png'),
                       pg.image.load('level/hard1.png')), ((305, 570), (430, 570), (555, 570)))
    setting_toggle = ToggleButton(80, 450, 100, 100, pg.image.load('setting.png'), ('âm lượng', 'nhạc nền'),
                         ((100, 570), (100, 610)),
                         ((225, 562), (225, 602)))
    while True:
        clock.tick(120)
        event_list = pg.event.get()
        # select_option = list1.update(event_list)
        screen.fill(WHITE)
        # list1.draw(screen)
        # draw_grid()
        if x == 0:
            draw_start_menu(screen)
        elif x == 1:
            draw_information_game(screen)
        elif x == 2:
            draw_rank(screen, rank_list)
        # draw_info()
        # draw_information_game(screen)
        # draw_rank(screen, rank_list)
        # draw_level(screen)
        for event in event_list:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                # if yes and not check_pos_in_circle((300, 500, 50), pg.mouse.get_pos()):
                #     yes = not yes
                if check_pos_in_circle((490, 500, 50), pg.mouse.get_pos()) and x == 0:
                    x = 2
                elif check_pos_in_circle((670, 500, 50), pg.mouse.get_pos()) and x == 0:
                    x = 1
                elif check_pos_in_circle((300, 500, 50), pg.mouse.get_pos()):
                    if x == 0:
                        yes_level = True
                    else:
                        yes_level = not yes_level
                elif check_pos_in_circle((130, 500, 50), pg.mouse.get_pos()):
                    if x == 0:
                        yes_setting = True
                    else:
                        yes_setting = not yes_setting
                else:
                    x = 0
        if yes_level and x == 0:
            selected_option = level_list.update(event_list)
            level_list.draw(screen)
        if yes_setting and x == 0:
            adj = setting_toggle.update(event_list)
            setting_toggle.draw(screen)
        pg.display.flip()
