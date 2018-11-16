import pygame
from pygame.locals import *
from constant import *
import numpy as np
from obstacle import Obstacle
from bird import Bird
from world import World

pygame.init()
screen = pygame.display.set_mode((W, H+HUD_H), DOUBLEBUF)
screen.set_alpha(None)
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 25)
hud_background = pygame.Rect(0, H, W, HUD_H)

class GeneticAlg(object):
    def __init__(self):
        self.birds = []
        for i in range(3):
            self.birds.append(Bird())
        self.gen = 0
        self.best_score = 0

    def simulate(self):
        world = World(self.birds)
        clock = pygame.time.Clock()
        done = False
        c=0
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                done = True
            if len([bird for bird in world.birds if bird.alive])==0:
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

            pygame.draw.rect(screen, (255, 255, 255), hud_background)
            screen.blit(score_surface, (2,H))
            best_score_srf = myfont.render("Best: {}".format(self.best_score),
                                               True, (0, 0, 0))
            screen.blit(best_score_srf, (2,H+20))
            gen_surface = myfont.render("Generation: {}".format(self.gen),
                                               True, (0, 0, 0))
            screen.blit(gen_surface, (W/2-60,H))
            fps_surface = myfont.render("FPS: {:.0f}".format(clock.get_fps()),
                                        True, (0, 0, 0))
            screen.blit(fps_surface, (W-65,H))

            pygame.display.flip()

        if c > self.best_score:
            self.best_score = c

    def get_fitness_score(self):
        pass

    def mutate(self):
        self.gen += 1
        for bird in self.birds:
            bird.__init__()
