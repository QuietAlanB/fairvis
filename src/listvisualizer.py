import pygame
import math
import algo

pygame.font.init()
font_size = 24
font = pygame.font.Font("res/Lexend-Light.ttf", font_size)

class ListVisualizer:
        def __init__(self, list):
                self.list = list

        # this assumes that no `self.list` element is >`screen_size[1]`.
        def draw_update(self, screen, screen_size, cur_algo):
                pillar_size = math.ceil(screen_size[0] / len(self.list))
                largest = max(self.list)

                for i, elem in enumerate(self.list):
                        height = elem / largest * screen_size[1]

                        x = pillar_size * i
                        y = screen_size[1] - height

                        # by default, draw color of element depending on size.
                        # but if the element was just swapped or compared, use
                        # a different, pre-programmed color.
                        col = (elem / largest * 255,) * 3
                        
                        for cmp in algo.ro_display_cmp_queue:
                                if i == cmp[0] or i == cmp[1]:
                                        col = (100, 100, 255)
                                        
                        for swap in algo.ro_display_swap_queue:
                                if i == swap[0] or i == swap[1]:
                                        col = (255, 0, 0)

                        pygame.draw.rect(
                                screen,
                                col,
                                (x, y, pillar_size, height)
                        )

                algo_dict = {
                        algo.bubble_sort: "Bubble sort",
                        algo.insertion_sort: "Insertion sort",
                        algo.gnome_sort: "Gnome sort",
                        algo.selection_sort: "Selection sort",
                }

                font_surface_algo = font.render(f"Current algorithm: {algo_dict[cur_algo]}", False, (255, 0, 0))
                font_surface_cmp = font.render(f"Comparisons: {algo.ro_comparisons}", False, (255, 0, 0))
                font_surface_swap = font.render(f"Swaps: {algo.ro_swaps}", False, (255, 0, 0))
                screen.blit(font_surface_algo, (0, 0))
                screen.blit(font_surface_cmp, (0, font_size))
                screen.blit(font_surface_swap, (0, font_size * 2))
