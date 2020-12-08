import pygame
from constants import *
from board import Board
import numpy as np
import os
from colorsys import *

pygame.init()


class ColorPicker:
    def __init__(self, wheel_pos, wheel_rad, slider_pos, slider_size, slider_horiz, slider_invert, cursor_rad, color1, display_rect_loc, display_rect_size=(150, 150)):
        self.wheel_pos, self.wheel_rad = wheel_pos, wheel_rad
        self.slider_pos, self.slider_size, self.slider_horiz, self.slider_invert = slider_pos, slider_size, slider_horiz, slider_invert
        self.cursor_rad = cursor_rad
        self.display_rect_loc, self.display_rect_size = display_rect_loc, display_rect_size
        if color1:
            self.wheel_cursor, self.slider_cursor = np.array((123, 274)), np.array((25, 230))
        else:
            self.wheel_cursor, self.slider_cursor = np.array((142, 193)), np.array((25, 31))
        self.slider_surf = pygame.Surface(slider_size)
        self.wheel_surf = pygame.transform.scale(
            pygame.image.load(os.path.join(os.path.realpath(os.path.dirname(__file__)), "assets", "color_picker.png")), (wheel_rad * 2,) * 2)
        self.cursor_surf = pygame.Surface((self.cursor_rad*2,)*2, pygame.SRCALPHA)
        self.wheel_darken = pygame.Surface((wheel_rad * 2,) * 2, pygame.SRCALPHA)
        self._create_wheel()
        self._create_slider()
        self.update_wheel()

    def draw(self, window):
        pygame.draw.rect(window, self.get_rgb(), (*self.display_rect_loc, *self.display_rect_size))
        window.blit(self.slider_surf, self.slider_pos)
        self._draw_cursor(window, np.array(self.slider_pos) + np.array(self.slider_cursor))
        window.blit(self.wheel_surf, self.wheel_pos)
        window.blit(self.wheel_darken, self.wheel_pos)
        self._draw_cursor(window, np.array(self.wheel_pos) + np.array(self.wheel_cursor))

    def update(self, window):
        self.draw(window)
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            if ((self.wheel_pos[0] + self.wheel_rad - x) ** 2 + (self.wheel_pos[1] + self.wheel_rad - y) ** 2)**0.5 < self.wheel_rad - 2:
                self.wheel_cursor = (x - self.wheel_pos[0], y - self.wheel_pos[1])
            elif self.slider_pos[0] < x < self.slider_pos[0] + self.slider_size[0] and self.slider_pos[1] < y < self.slider_pos[1] + self.slider_size[1]:
                self.slider_cursor[1] = y - self.slider_pos[1]
                self.update_wheel()

    def get_rgb(self):
        wrgb = self.wheel_surf.get_at(self.wheel_cursor)
        srgb = self.slider_surf.get_at(self.slider_cursor)
        whsv = rgb_to_hsv(*(np.array(wrgb)/255)[:3])
        shsv = rgb_to_hsv(*(np.array(srgb)/255)[:3])
        hsv = (whsv[0], whsv[1], shsv[2])
        rgb = np.array(hsv_to_rgb(*hsv))*255
        return rgb

    def get_hsv(self):
        rgb = (np.array(self.get_rgb())/255)[:3]
        return np.array(rgb_to_hsv(*rgb))*255

    def update_wheel(self):
        pygame.draw.circle(self.wheel_darken, (0, 0, 0, np.interp(
            self.get_hsv()[2], (0, 255), (255, 0))), (self.wheel_rad,)*2, self.wheel_rad)

    def _create_wheel(self):
        pygame.draw.circle(self.wheel_surf, (0, 0, 0),
                           (self.wheel_rad,)*2, self.wheel_rad, 2)

    def _create_slider(self):
        w, h = self.slider_size
        if self.slider_horiz:
            for x in range(w):
                if self.slider_invert:
                    value = np.interp(x, (0, w), (0, 255))
                else:
                    value = np.interp(x, (0, w), (255, 0))
                pygame.draw.rect(self.slider_surf, (value,)*3, (x, 0, 1, h))

        else:
            for y in range(h):
                if self.slider_invert:
                    value = np.interp(y, (0, h), (0, 255))
                else:
                    value = np.interp(y, (0, h), (255, 0))
                pygame.draw.rect(self.slider_surf, (value,)*3, (0, y, w, 1))
        pygame.draw.rect(self.slider_surf, (0, 0, 0), (0, 0, w, h), 1)

    def _draw_cursor(self, window, pos):
        pygame.draw.circle(window, (255, 255, 255), pos, self.cursor_rad)
        pygame.draw.circle(window, (0, 0, 0), pos, self.cursor_rad, 2)


class Checkbox:
    def __init__(self, loc, size, color=(255, 255, 255), text_col=(0, 0, 0), check_col=(0, 0, 0), padding=5, text="Checkbox", font=pygame.font.SysFont("comicsans", 80)):
        self.loc, self.size = loc, size
        self.text = text
        self.font = font
        self.color = color
        self.text_col = text_col
        self.padding = padding
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(os.path.realpath(os.path.dirname(__file__)), "assets", "checkmark.png")), (size[0] - padding*2, size[1] - padding*2))
        self.checked = False
        if check_col != (0,)*3:
            self.change_check_color(check_col)

    def draw(self, window, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pygame.Rect(*self.loc, *self.size).collidepoint(event.pos):
                        self.checked = not self.checked

        pygame.draw.rect(window, self.color, (*self.loc, *self.size))
        text = self.font.render(self.text, 1, self.text_col)
        window.blit(text, (self.loc[0] + self.size[0] + 5, self.loc[1] + self.size[1]//2 - text.get_height()//2))
        if self.checked:
            window.blit(self.image, (self.loc[0] + self.padding, self.loc[1] + self.padding))

    def change_check_color(self, check_col):
        w, h = self.image.get_size()
        for x in range(w):
            for y in range(h):
                if self.image.get_at((x, y))[3] != 0:
                    self.image.set_at((x, y), check_col)


class Slider:
    def __init__(self, rect_loc, rect_size, rect_col=(128, 128, 128), circle_col=(255, 255, 255), val_range=(1, 100), initial_val=20, font=None, text=None, text_col=(0, 0, 0), text_val=False, horiz=True):
        self.x, self.y = int(rect_loc[0]), int(rect_loc[1])
        self.width, self.height = int(rect_size[0]), int(rect_size[1])
        self.rectCol, self.circleCol = rect_col, circle_col
        self.valRange = val_range[0], val_range[1] + 1
        self.value = initial_val
        self.font, self.text = font, text
        self.text_col = text_col
        self.textVal = text_val
        self.radius = int(self.height/2) if horiz else int(self.width/2)
        self.radius += 3
        self.horiz = horiz

    def get_value(self):
        return self.value

    def draw(self, window):
        if pygame.mouse.get_pressed()[0]:
            if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(pygame.mouse.get_pos()):
                self.value = int(np.interp(pygame.mouse.get_pos()[0], (self.x, self.x + self.width), self.valRange)) if self.horiz else int(
                    np.interp(pygame.mouse.get_pos()[1], (self.y, self.y + self.height), self.valRange))

        pygame.draw.rect(window, self.rectCol, (int(self.x), int(
            self.y), int(self.width), int(self.height)))

        if self.horiz:
            circle_x = np.interp(
                self.value, self.valRange, (self.x, self.x + self.width))
            pygame.draw.circle(window, self.circleCol, (int(
                circle_x), int(self.y + self.height/2)), int(self.radius))

        else:
            circle_y = np.interp(
                self.value, self.valRange, (self.y, self.y + self.height))
            pygame.draw.circle(window, self.circleCol, (int(
                self.x + self.width/2), int(circle_y)), int(self.radius))

        if self.font is not None and self.text is not None:
            text = self.font.render(self.text + ": " + str(self.get_value()) if self.textVal else self.text, 1, self.text_col)
            window.blit(text, (int(self.x + self.width/2 -
                                   text.get_width()/2), int(self.y + self.height + 5)))


class Interface:
    x, y = 1000, 0
    width, height = 500, 1000
    board = Board(0, 0, 1000, 1000)
    rows = Slider((1250 - 235, 120), (275, 35), val_range=(4, 40), initial_val=8, font=pygame.font.SysFont("comicsans", 35), text="Rows", text_col=(255, 255, 255), text_val=True)
    cols = Slider((1250 - 235, 200), (275, 35), val_range=(4, 40), initial_val=8, font=pygame.font.SysFont("comicsans", 35), text="Columns", text_col=(255, 255, 255), text_val=True)
    sync = Checkbox((1320, 355/2 - 15), (35, 35), text="Sync", text_col=(255, 255, 255), font=pygame.font.SysFont("comicsans", 30))
    color1 = ColorPicker((1250 - 235, 400 - 80), 150, (1250 - 235 + 300 + 20, 400 - 80), (50, 300), False, False, 5, False, (0, 0), (0, 0))
    color2 = ColorPicker((1250 - 235, 720 - 40), 150, (1250 - 235 + 300 + 20, 720 - 40), (50, 300), False, False, 5, True, (0, 0), (0, 0))
    label_font = pygame.font.SysFont("comicsans", 30)

    def __init__(self, window):
        self.window = window

    def start(self):
        clock = pygame.time.Clock()

        while True:
            clock.tick(FPS)
            self.update()
            pygame.display.update()

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.draw(self.window)
        self.board.draw(self.window, self.color1.get_rgb(), self.color2.get_rgb())
        self.board.knight.update(self.window, events)
        self.sync.draw(self.window, events)
        self.rows.draw(self.window)
        self.cols.draw(self.window)
        if self.sync.checked:
            val = (self.rows.value + self.cols.value)//2
            self.rows.value = self.cols.value = val
        self.color1.update(self.window)
        self.color2.update(self.window)
        text = self.label_font.render("Small Color", 1, self.color1.get_rgb())
        self.window.blit(text, (1250 - 235 + 150 - text.get_width()//2, 400 - 80 - text.get_height() - 5))
        text = self.label_font.render("Big Color", 1, self.color2.get_rgb())
        self.window.blit(text, (1250 - 235 + 150 - text.get_width()//2, 720 - 40 - text.get_height() - 5))
        self.board.change_rowcol(self.rows.get_value(), self.cols.get_value())

    def draw(self, window):
        window.fill(WHITE)
        window.fill(BLACK, (1000, 0, 500, 1000))
