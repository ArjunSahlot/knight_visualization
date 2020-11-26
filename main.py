import pygame
from knight_visualization.constants import *


# Window Management
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("knight_visualization")


def draw_window(win):
    win.fill(WHITE)


def main(win, width, height):
    pygame.init()
    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)
        draw_window(win)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        pygame.display.update()


main(WINDOW, WIDTH, HEIGHT)
