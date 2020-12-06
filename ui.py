import pygame
from constants import *
from board import Board
import numpy as np

pygame.init()


class Slider:
    def __init__(self, rect_loc, rect_size, rect_col=(128, 128, 128), circle_col=(255, 255, 255), val_range=(1, 100), initial_val=20, font=None, text=None, text_col=(0, 0, 0), text_val=False, horiz=True):
        self.x, self.y = int(rect_loc[0]), int(rect_loc[1])
        self.width, self.height = int(rect_size[0]), int(rect_size[1])
        self.rectCol, self.circleCol = rect_col, circle_col
        self.valRange = val_range[0], val_range[1] + 1
        self.value = initial_val
        self.font, self.text = font, text
        self.textCol = text_col
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
            circleX = np.interp(
                self.value, self.valRange, (self.x, self.x + self.width))
            pygame.draw.circle(window, self.circleCol, (int(
                circleX), int(self.y + self.height/2)), int(self.radius))

        else:
            circleY = np.interp(
                self.value, self.valRange, (self.y, self.y + self.height))
            pygame.draw.circle(window, self.circleCol, (int(
                self.x + self.width/2), int(circleY)), int(self.radius))

        if self.font is not None and self.text is not None:
            text = self.font.render(self.text + ": " + str(self.get_value()) if self.textVal else self.text, 1, self.textCol)
            window.blit(text, (int(self.x + self.width/2 -
                                   text.get_width()/2), int(self.y + self.height + 5)))


class Interface:
    x, y = 1000, 0
    width, height = 500, 1000
    board = Board(0, 0, 1000, 1000, (255, 188, 163), (24, 0, 0))
    rows = Slider((1250 - 200, 120), (400, 35), val_range=(4, 40), initial_val=8, font=pygame.font.SysFont("comicsans", 35), text="Rows", text_col=(255, 255, 255), text_val=True)
    cols = Slider((1250 - 200, 200), (400, 35), val_range=(4, 40), initial_val=8, font=pygame.font.SysFont("comicsans", 35), text="Columns", text_col=(255, 255, 255), text_val=True)

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
        self.board.draw(self.window)
        self.board.knight.update(self.window, events)
        self.rows.draw(self.window)
        self.cols.draw(self.window)
        self.board.change_rowcol(self.rows.get_value(), self.cols.get_value())

    def draw(self, window):
        window.fill(WHITE)
        window.fill(BLACK, (1000, 0, 500, 1000))
