import pygame
import math

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
                        pygame.draw.rect(
                                screen,
                                (255, 255, 255),
                                (x, y, pillar_size, height)
                        )
