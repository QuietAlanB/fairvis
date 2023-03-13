import pygame

screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()
running = True

while running:
        for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                        running = False

        pygame.display.update()
        clock.tick(60)