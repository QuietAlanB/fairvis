import pygame
import random
import algo
from threading import Thread
from listvisualizer import ListVisualizer

pygame.init()

screen_size = (900, 600)
screen = pygame.display.set_mode(screen_size)
running = True

lst = []
for i in range(120):
        lst.append(random.randint(1, screen_size[1]))

list_vis = ListVisualizer(lst)
algo_thread = Thread(target = algo.bubble_sort, args = [lst])

algo_thread.start()

while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False
                        algo.wo_terminate = True
                        
        if algo.ro_display_ready:
                screen.fill((0, 0, 0))
                list_vis.draw_update(screen, screen_size)
                algo.wo_display_done = True

        pygame.display.update()

algo_thread.join()
