import pygame
import random
import algo
from threading import Thread
from listvisualizer import ListVisualizer

pygame.init()

screen_size = (1920, 1080)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("sorting algorithm visualizer")
pygame.display.set_icon(pygame.image.load("res/fairvislogo.png"))
running = True

lst = []
for i in range(60):
        lst.append(i)

random.shuffle(lst)

list_vis = ListVisualizer(lst)

cur_algo = algo.bubble_sort
algo_thread = Thread(target = cur_algo, args = [lst])
algo_thread.start()

while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False
                        algo.wo_terminate = True

                key_down = event.type == pygame.KEYDOWN
                key_up = event.type == pygame.KEYUP

                # closes the thread
                if key_down and event.key == pygame.K_SPACE:
                        if (algo_thread.is_alive()):
                                algo.wo_terminate = True

                # starts a new thread
                if key_up and event.key == pygame.K_SPACE:
                        random.shuffle(lst)

                        algo_thread = Thread(target = cur_algo, args = [lst])
                        algo_thread.start()
                        
        if algo.ro_display_ready:
                screen.fill((0, 0, 0))
                list_vis.draw_update(screen, screen_size, cur_algo)
                algo.wo_display_done = True

        pygame.display.update()

algo_thread.join()
