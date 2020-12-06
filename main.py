import pygame
from constants import *
from ui import Interface


# Window Management
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Knight Visualizer")


def main(window):
    interface = Interface(window)
    interface.start()


main(WINDOW)
