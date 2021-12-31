import sys

import pygame as pg
import random

s_width = 800
s_height = 700
play_width = 300
play_height = 600
block_size = 30
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height
number_screen = 0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 51, 51)
LGRAY = (230, 230, 250)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
LBLUE = (30, 144, 255)
play_button_pos = ((s_width - 150) // 2 + 75, 230 + 75, 75)
ranking_button_pos = (490, 500, 50)
information_button_pos = (670, 500, 50)
level_button_pos = (300, 500, 50)
setting_button_pos = (130, 500, 50)
button_pos = [play_button_pos, setting_button_pos, level_button_pos, ranking_button_pos, information_button_pos, ]

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

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(255, 60, 60), (255, 150, 60), (255, 255, 50), (160, 255, 128), (0, 180, 255), (166, 120, 255),
                (140, 220, 255), (255, 150, 220)]

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((s_width, s_height))
pg.display.set_caption('T E T I S')


def check_pos_in_circle(cir_pos, mouse_pos):
    return (mouse_pos[0] - cir_pos[0]) ** 2 + (mouse_pos[1] - cir_pos[1]) ** 2 <= cir_pos[2] ** 2


class OptionBox:

    def __init__(self, x, y, w, h, choose, list_level, option_list, pos_option_list=(), selected=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.circle_pos = (x + 50, y + 50, 50)
        self.level_list = list_level
        self.option_list = option_list
        self.selected = selected
        self.choose = choose
        self.rect = pg.Rect(self.x - 10, self.y + self.choose[0].get_height() - 20, 180 + len(self.option_list) * 80,
                            160)
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1
        self.pos_clicked = (x + 50, y + 50)
        self.pos_option_list = pos_option_list
        self.effect = False

    def draw(self, surface):
        idx = 1 if self.effect else 0
        radius_effect = 0 if idx == 0 else 10
        surface.blit(self.choose[idx], (self.x + radius_effect, self.y + radius_effect))
        if self.draw_menu:
            pg.draw.rect(surface, WHITE,
                         (self.x, self.y + self.choose[0].get_height(), 180 + len(self.option_list) * 80, 160))
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
            if event_item.type == pg.MOUSEMOTION:
                if check_pos_in_circle(level_button_pos, pg.mouse.get_pos()):
                    self.effect = True
                else:
                    self.effect = False
            elif event_item.type == pg.MOUSEBUTTONDOWN:
                if self.draw_menu and self.active_option >= 0:
                    self.selected = self.active_option
                    self.draw_menu = False
                    self.choose[0] = self.level_list[self.active_option]
                    # print(self.active_option)
                    return self.active_option
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
            elif event_item.type == pg.MOUSEBUTTONUP:
                self.pos_clicked = pg.mouse.get_pos()
        return -1


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


class Piece(object):
    rows = 20
    columns = 10

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    grid = [[(255, 255, 255) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (255, 255, 255)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    global shapes, shape_colors
    # return Piece(5, 0, random.choice(shapes))
    return Piece(5, 0, shapes[2])


def draw_text_middle(text, size, color, surface):
    font = pg.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (
        top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))


def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pg.draw.line(surface, (128, 128, 128), (sx, sy + i * 30), (sx + play_width, sy + i * 30))
        for j in range(col):
            pg.draw.line(surface, (128, 128, 128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))


def clear_rows(grid, locked, score):
    inc = 0
    ind_delete_row = []
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        # Clear if there is no white pixels in the row
        if (255, 255, 255) not in row:
            inc += 1
            ind_delete_row.append(i)
            score[0] = score[0] + 10
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        clear_row_sound = pg.mixer.Sound("clear.wav")
        clear_row_sound.play()
        for ind in ind_delete_row[::-1]:
            for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + 1)
                    locked[newKey] = locked.pop(key)
    return ind_delete_row


def draw_right_side(shape, surface, score):
    # Preview Next Shape
    font = pg.font.SysFont('comicsans', 30)

    label = font.render('Next Shape', 1, (255, 255, 255))

    sx = top_left_x + play_width
    sy = s_height / 2
    l = (s_width - play_width) / 2
    x = sx + l / 2
    x_line = sx + l / 2 - 2.5 * block_size
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pg.draw.rect(surface, shape.color,
                             (x_line + j * block_size, sy + i * block_size, block_size, block_size), 0)
    for i in range(6):
        pg.draw.line(surface, (64, 64, 64), (x_line, sy + i * block_size),
                     (x_line + 6 * block_size, sy + i * block_size))
        for j in range(6):
            pg.draw.line(surface, (64, 64, 64), (x_line + j * block_size, sy),
                         (x_line + j * block_size, sy + 6 * block_size))
    surface.blit(label, (x - label.get_width() / 2, sy - block_size - 20))

    # Preview Score
    label1 = font.render("SCORE", 1, (255, 255, 255))
    label2 = font.render(score, 1, (255, 255, 255))

    surface.blit(label1, (x - label1.get_width() / 2, sy + 5 * block_size))
    surface.blit(label2, (x - label2.get_width() / 2, sy + 6 * block_size))


def draw_score(surface, score):
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    font = pg.font.SysFont('comicsans', 30)
    label1 = font.render("SCORE", 1, (255, 255, 255))
    label2 = font.render(str(score[0]), 1, (255, 255, 255))
    surface.blit(label1, (sx + 35, sy + 150))
    surface.blit(label2, (sx + 70, sy + 180))


def draw_score_board(surface):
    surface_score = pg.Surface((200, 170))
    surface_score.fill((64, 64, 64))

    black_board = pg.image.load('blackboard.png')
    teacher = pg.image.load('teacher.png')
    surface_score.blit(black_board, (50, 0))
    surface_score.blit(teacher, (0, 70))
    surface.blit(surface_score, (20, top_left_y))


def draw_window(surface, ind_del_row=[]):
    surface.fill((64, 64, 64))
    draw_score_board(surface)
    label = pg.image.load('tetris.png')
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 17))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pg.draw.rect(surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)
    draw_grid(surface, 20, 10)
    pg.draw.rect(surface, (100, 100, 100), (top_left_x, top_left_y, play_width, play_height), 5)


def effect_del_rows(surface, ind_del_rows, effect):
    # draw_info()
    ind_del_rows.sort()
    surface.fill((64, 64, 64))
    draw_score_board(surface)
    label = pg.image.load('tetris.png')
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 17))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pg.draw.rect(surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)

    surface.blit(pg.transform.scale(effect, (play_width, 30 * len(ind_del_rows))),
                 ((s_width - play_width) // 2, top_left_y + 30 * ind_del_rows[0]))
    draw_grid(surface, 20, 10)
    pg.draw.rect(surface, (100, 100, 100), (top_left_x, top_left_y, play_width, play_height), 5)


def calculate_level_and_fall_speed(score, difficult):
    if difficult == 1:
        level = 1
    elif difficult == 2:
        level = 11
    elif difficult == 3:
        level = 21
    level = int(score[0] / 100) + 1
    fall_speed = 0.27 - (level * 0.02)
    return fall_speed


def play_game(Score):
    global grid, x, concac
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pg.time.Clock()
    fall_time = 0
    fall_speed = 0.27

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                # fall_sound = pg.mixer.Sound("fall.wav")
                # fall_sound.play()
                current_piece.y -= 1
                change_piece = True

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.display.quit()
                quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pg.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pg.K_UP:
                    # rotate shape
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
                elif event.key == pg.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
        ind_del_rows = []
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            ind_del_rows = clear_rows(grid, locked_positions, Score)
            fall_speed = 0.27  # calculate_level_and_fall_speed(Score)

        if len(ind_del_rows) > 0:
            t = pg.time.get_ticks()
            while t + 250 >= pg.time.get_ticks():
                effect_del_rows(screen, ind_del_rows, pg.image.load('e3.png'))
                pg.display.update()
            while t + 500 >= pg.time.get_ticks():
                effect_del_rows(screen, ind_del_rows, pg.image.load('e2.png'))
                pg.display.update()
            while t + 750 >= pg.time.get_ticks():
                effect_del_rows(screen, ind_del_rows, pg.image.load('e3.png'))
                pg.display.update()

        draw_window(screen, ind_del_rows)
        score = str(Score[0])
        draw_right_side(next_piece, screen, score)
        pg.display.update()

        if check_lost(locked_positions):
            run = False

    pg.mixer.music.stop()
    loose_sound = pg.mixer.Sound("gameover.wav")
    loose_sound.play()
    draw_text_middle("You Lost : " + str(Score[0]), 40, (0, 0, 0), screen)
    pg.display.update()
    pg.time.delay(2000)
    pg.mixer.music.play()

if __name__ == '__main__':
    # main()
    # global x, move, count, y_text
    pg.mixer.init()
    pg.mixer.music.load("nen.wav")
    pg.mixer.music.set_volume(0.0)
    pg.mixer.music.play(-1, 0.0)
    Score = [0]
    yes_level = False
    yes_setting = False
    volume = True
    move = 0
    count = 0
    label = pg.image.load('tetris_big.png')
    rank_list = [122333, 1232341, 5432344, 5623453, 3654234234]
    button_list = {(pg.image.load('play.png'), pg.image.load('play_effect.png')): False,
                   (pg.image.load('setting.png'), pg.image.load('setting_effect.png')): False,
                   (pg.image.load('level/level.png'), pg.image.load('level/level_effect.png')): False,
                   (pg.image.load('rank/ranking.png'), pg.image.load('rank/ranking_effect.png')): False,
                   (pg.image.load('information.png'), pg.image.load('information_effect.png')): False}
    rank_list.sort(reverse=True)
    level_list = OptionBox(250, 450, 100, 100,
                           [pg.image.load('level/level.png'), pg.image.load('level/level_effect.png')], (
                               pg.image.load('level/easy.png'), pg.image.load('level/medium.png'),
                               pg.image.load('level/hard.png')),
                           (pg.image.load('level/easy1.png'), pg.image.load('level/medium1.png'),
                            pg.image.load('level/hard1.png')), ((305, 570), (430, 570), (555, 570)))
    pg.time.set_timer(pg.USEREVENT, 40)

    while True:
        clock.tick(120)
        event_list = pg.event.get()
        screen.fill(WHITE)
        screen.blit(label, ((s_width - label.get_width()) // 2, 30 + move))
        # if yes_level and number_screen == 0:
        selected_option = level_list.update(event_list)
        level_list.draw(screen)
        if number_screen == 0:
            for i, button in enumerate(button_list, 0):
                if i == 2:
                    continue
                idx = 1 if button_list.get(button) else 0
                radius = 75 if i == 0 else 50
                radius_effect = 0 if idx == 0 else 10
                screen.blit(button[idx],
                            (button_pos[i][0] - radius + radius_effect, button_pos[i][1] - radius + radius_effect))

        elif number_screen == 1:
            draw_information_game(screen)
        elif number_screen == 2:
            draw_rank(screen, rank_list)
        elif number_screen == 3:
            play_game(Score)

        for event in event_list:
            if event.type == pg.QUIT:
                pg.display.quit()
                quit()

            if event.type == pg.MOUSEMOTION:
                for i, button in enumerate(button_list, 0):
                    if check_pos_in_circle(button_pos[i], pg.mouse.get_pos()):
                        button_list[button] = True
                    else:
                        button_list[button] = False

            if event.type == pg.MOUSEBUTTONDOWN:
                if check_pos_in_circle(play_button_pos, pg.mouse.get_pos()):
                    number_screen = 3
                elif check_pos_in_circle(ranking_button_pos, pg.mouse.get_pos()) and number_screen == 0:
                    number_screen = 2
                elif check_pos_in_circle(information_button_pos, pg.mouse.get_pos()) and number_screen == 0:
                    number_screen = 1
                elif check_pos_in_circle(level_button_pos, pg.mouse.get_pos()):
                    if number_screen == 0:
                        yes_level = True
                    else:
                        yes_level = not yes_level
                elif check_pos_in_circle(setting_button_pos, pg.mouse.get_pos()):
                    if number_screen == 0:
                        yes_setting = True
                    else:
                        yes_setting = not yes_setting
                else:
                    number_screen = 0

            if event.type == pg.USEREVENT:
                if count == 0:
                    move += 1
                    if move == 10:
                        count = 1
                else:
                    move -= 1
                    if move == 0:
                        count = 0

        pg.display.flip()
