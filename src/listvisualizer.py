import pygame
import math
import algo

pygame.font.init()
font_size = 30
font = pygame.font.Font("res/Lexend-Bold.ttf", font_size)

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
                        col = elem / largest * 255

                        pygame.draw.rect(
                                screen,
                                (col, col, col),
                                (x, y, pillar_size, height)
                        )

                algo_dict = {algo.bubble_sort: "Bubble sort"}
                cur_algo_str = algo_dict[cur_algo]

                font_surface_algo = font.render(f"Current algorithm: {cur_algo_str}", False, (255, 0, 0))
                font_surface_iter = font.render(f"Iterations: {algo.ro_iterations}", False, (255, 0, 0))
                font_surface_cmp = font.render(f"Comparisons: {algo.ro_comparisons}", False, (255, 0, 0))
                font_surface_swap = font.render(f"Swaps: {algo.ro_swaps}", False, (255, 0, 0))
                screen.blit(font_surface_algo, (0, 0))
                screen.blit(font_surface_iter, (0, font_size))
                screen.blit(font_surface_cmp, (0, font_size * 2))
                screen.blit(font_surface_swap, (0, font_size * 3))
