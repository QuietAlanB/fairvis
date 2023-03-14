import pygame
from listvisualizer import ListVisualizer
from algo import *
screen_size = (1920, 1080)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
running = True

lst = []

for i in range(900):
        lst.append(i)

lst.reverse()

list_vis = ListVisualizer(lst)

while running:
        for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                        running = False

        list_vis.draw_update(screen, screen_size)

        pygame.display.update()
        clock.tick(60)