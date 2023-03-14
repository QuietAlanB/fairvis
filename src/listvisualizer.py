import pygame
import math
import algo

pygame.font.init()
font = pygame.font.Font("res/Lexend-Bold.ttf", 30)

class ListVisualizer:
        def __init__(self, list):
                self.list = list

        # this assumes that no `self.list` element is >`screen_size[1]`.
        def draw_update(self, screen, screen_size):
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

                font_surface_iter = font.render(f"Iterations: {algo.ro_iterations}", False, (255, 0, 0))
                font_surface_cmp = font.render(f"Comparisons: {algo.ro_comparisons}", False, (255, 0, 0))
                font_surface_swap = font.render(f"Swaps: {algo.ro_swaps}", False, (255, 0, 0))
                screen.blit(font_surface_iter, (0, 0))
                screen.blit(font_surface_cmp, (0, 30))
                screen.blit(font_surface_swap, (0, 60))
