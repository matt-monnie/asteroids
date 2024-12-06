# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from player import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Player.containers = (updatable, drawable)

    game_clock = pygame.time.Clock()
    dt = 0

    while(True):
        screen.fill((0,0,0))
        for obj in updatable:
            obj.update(dt)
        for obj in drawable:
            obj.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pygame.display.flip()
        dt = game_clock.tick(60) / 1000


if __name__ == "__main__":
    main()
