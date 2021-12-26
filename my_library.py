import pygame as pg


def check_pos_in_circle(cir_pos, mouse_pos):
    return (mouse_pos[0] - cir_pos[0]) ** 2 + (mouse_pos[1] - cir_pos[1]) ** 2 <= cir_pos[2] ** 2


class OptionBox:

    def __init__(self, x, y, w, h, choose, list_level, option_list, selected=0):
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
        self.space = 180 // (len(self.option_list) + 1)
        self.pos_clicked = (x + 50, y + 50)

    def draw(self, surface):
        surface.blit(self.choose, (self.x, self.y))
        if self.draw_menu:
            surface.blit(pg.transform.scale(pg.image.load('level/bg.png'), (180 + len(self.option_list) * 80, 160)),
                         (self.x, self.y + self.choose.get_height() - 20))
            for i, value in enumerate(self.option_list, 0):
                surface.blit(value, (self.x + self.space + i * 80 + self.space * i, self.y + 120))
                # print((140 + i * 100 + 30 * i, 220))

    def update(self, list_event):
        mouse_pos = pg.mouse.get_pos()
        self.menu_active = check_pos_in_circle(self.circle_pos, mouse_pos)
        self.active_option = -1
        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.menu_active = True if check_pos_in_circle((self.x + 50, self.y + 50, 50), self.pos_clicked) else False
            for i in range(len(self.option_list)):
                if check_pos_in_circle((self.x + self.space + i * 80 + self.space * i + 40, self.y + 120 + 40, 40),
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
                    print(self.active_option)
                    return self.active_option
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
            if event_item.type == pg.MOUSEBUTTONUP:
                self.pos_clicked = pg.mouse.get_pos()

        return -1
