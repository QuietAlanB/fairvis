import pygame

class ListVisualizer:
        def __init__(self, list):
                self.list = list

        def draw_update(self, screen, screen_size):
                max_size = screen_size[0]
                size = len(self.list)
                step = int(max_size / size)
                ratio = (9/16)

                for i in range(0, size):
                        value = self.list[i] + 1
                        scaled_value = value * ratio * step

                        pygame.draw.rect(
                                screen, (255, 255, 255),
                                (i * step, screen_size[1] - scaled_value, step, scaled_value)
                        )