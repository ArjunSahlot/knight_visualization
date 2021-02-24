#
#  Knight visualizer
#  A pygame project that shows you graphically how many moves it takes a knight to move to a specific square on the chess board.
#  Copyright Arjun Sahlot 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import pygame
import os
from constants import *
from movegen import square_dist
from numpy import max as maximum, interp as map_range

pygame.init()


class Knight:
    moving = False
    color = True
    factor = 80
    white_image = pygame.image.load(os.path.join("assets", "white_knight.png"))
    black_image = pygame.image.load(os.path.join("assets", "black_knight.png"))

    def __init__(self, board):
        self.board = board
        self.factor /= 100
        self.white = self.black = None
        self.pos = None
        self.update_images()

    def update_images(self):
        sq_width, sq_height = self.board.width/self.board.cols, self.board.height/self.board.rows
        size = (int(sq_width * self.factor), int(sq_height * self.factor))
        self.pos = (0, 0)
        self.white = pygame.transform.scale(self.white_image, size)
        self.black = pygame.transform.scale(self.black_image, size)

    def calc_xy(self):
        sq_width, sq_height = self.board.width/self.board.cols, self.board.height/self.board.rows
        return self.pos[1] * sq_width + sq_width/2 - self.white.get_width()/2, self.pos[0] * sq_height + sq_height/2 - self.white.get_height()/2

    def update(self, window, events):
        mx, my = pygame.mouse.get_pos()
        sq_width, sq_height = self.board.width/self.board.cols, self.board.height/self.board.rows
        if self.moving:
            col = min(int(mx / sq_width), self.board.cols-1)
            row = int(my / sq_height)
            self.pos = row, col
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                self.moving = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(self.pos[1] * sq_width, self.pos[0] * sq_height, sq_width, sq_height).collidepoint(mx, my):
                    self.moving = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.color = not self.color
        self.draw(window)

    def draw(self, window):
        mx, my = pygame.mouse.get_pos()
        window.blit(self.white if self.color else self.black, (mx - self.board.width/self.board.cols/2, my - self.board.height/self.board.rows/2) if self.moving else self.calc_xy())


class Board:
    moves = []
    font = pygame.font.SysFont("comicsans", 100)
    factorx = 60
    factory = 70

    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.rows = self.cols = 8
        self.knight = Knight(self)
        self.factorx /= 100
        self.factory /= 100
        self.generate_moves()

    def change_rowcol(self, rows, cols):
        if rows != self.rows or cols != self.cols:
            self.rows, self.cols = rows, cols
            self.knight.update_images()
            self.generate_moves()

    def draw(self, window, col1, col2):
        sq_width, sq_height = self.width/self.cols, self.height/self.rows
        if self.knight.moving:
            self.generate_moves()

        for row in range(self.rows):
            for col in range(self.cols):
                dist = self.moves[row][col]
                if dist:
                    r = map_range(dist, (1, maximum(self.moves)), (col1[0], col2[0]))
                    g = map_range(dist, (1, maximum(self.moves)), (col1[1], col2[1]))
                    b = map_range(dist, (1, maximum(self.moves)), (col1[2], col2[2]))
                    color = (r, g, b)
                else:
                    color = (134, 216, 119)

                pygame.draw.rect(window, color, (sq_width*col, sq_height*row, sq_width, sq_height))
                w = sq_width * self.factorx
                h = sq_height * self.factory
                num = pygame.transform.scale(self.font.render(str(dist), 1, WHITE if self.knight.color else BLACK), (int(w), int(h)))
                if dist:
                    window.blit(num, (sq_width*(col + 0.5) - num.get_width()/2, sq_height*(row + 0.5) - num.get_height()/2))

        for x in range(self.cols + 1):
            pygame.draw.line(window, (85, 56, 52), (x * sq_width, self.y), (x * sq_width, self.y + self.height), 3)

        for y in range(self.rows + 1):
            pygame.draw.line(window, (85, 56, 52), (self.x, y * sq_height), (self.x + self.width, y * sq_height), 3)

    def generate_moves(self):
        self.moves = []
        for row in range(self.rows):
            self.moves.append([])
            for col in range(self.cols):
                self.moves[row].append(square_dist(self.knight.pos, (row, col), self.rows, self.cols))

        return self.moves
