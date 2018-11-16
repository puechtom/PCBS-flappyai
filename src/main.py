import pygame
from pygame.locals import *
import numpy as np
from copy import deepcopy
from bird import Bird
from obstacle import Obstacle
from world import World
from constant import *

pygame.init()
screen = pygame.display.set_mode((W, H+HUD_H), DOUBLEBUF)
screen.set_alpha(None)
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

hud_background = pygame.Rect(0, H, W, HUD_H)

c = 0
max_speed = 50
speed = SPEED

screen.fill(BG_COLOR)
pygame.display.flip()
pygame.time.wait(1000)

score_filename = "../data/score.txt"
f = open(score_filename, "r")
best_score = int(f.read().split()[0])
f.close()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 25)
best_score_surface = myfont.render("Best: {}".format(best_score),
                                   True, (0, 0, 0))

world = World()

clock = pygame.time.Clock()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        done = True

    dt = clock.tick(60)
    screen.fill(BG_COLOR)

    c+=1
    score_surface = myfont.render("Score: {}".format(c), True, (0, 0, 0))

    if pygame.key.get_pressed()[pygame.K_SPACE]:
        for bird in [bird for bird in world.birds if bird.alive]:
            bird.jump()

    world.update(dt)
    world.draw(screen)

    if len([bird for bird in world.birds if bird.alive]) == 0:
        if c > best_score:
            f = open(score_filename, "w")
            f.write(str(c))
            f.close()
            best_score = c
            best_score_surface = myfont.render("Best: {}".format(best_score),
                                               True, (0, 0, 0))
        c = 0
        world.__init__()
        # valid_birds = deepcopy(birds)
        # for bird in valid_birds:
        #     bird.__init__()
        pygame.time.wait(1000)
        clock = pygame.time.Clock()

    pygame.draw.rect(screen, (255, 255, 255), hud_background)

    screen.blit(score_surface, (2,H))
    screen.blit(best_score_surface, (2,H+20))
    fps_surface = myfont.render("FPS: {:.0f}".format(clock.get_fps()),
                                True, (0, 0, 0))
    screen.blit(fps_surface, (W-65,H))

    pygame.display.flip()
