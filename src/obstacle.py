import pygame
from pygame.locals import *
from constant import *
import numpy as np

class Block(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect

class Obstacle(object):
    # TODO: kill block when out of the screen

    def __init__(self, w=round(20), h=round(H/3), margin=round(H/10)):
        self.h = h
        self.w = w
        self.x = W+self.w
        self.y = np.random.randint(h/2+margin, H-h/2-margin)
        self.color = BLOCK_COLOR
        self.last = True
        self.upper = Block(pygame.Rect(self.x-self.w/2,
                                       0,
                                       self.w,
                                       self.y-self.h/2))
        self.lower = Block(pygame.Rect(self.x-self.w/2,
                                       self.y+self.h/2,
                                       self.w,
                                       H-(self.y+self.h/2)))
        self.group = pygame.sprite.Group()
        self.group.add(self.upper)
        self.group.add(self.lower)
        self.dist = 0
        self.height = 0

    def update(self, dt, speed=SPEED):
        self.vx = speed
        self.x -= self.vx * dt * BOOST
        self.x = round(self.x)

    def draw(self, output):
        self.upper = Block(pygame.Rect(self.x-self.w/2,
                                       0,
                                       self.w,
                                       self.y-self.h/2))
        self.lower = Block(pygame.Rect(self.x-self.w/2,
                                       self.y+self.h/2,
                                       self.w,
                                       H-(self.y+self.h/2)))
        self.group = pygame.sprite.Group()
        self.group.add(self.upper)
        self.group.add(self.lower)
        pygame.draw.rect(output, self.color, self.upper)
        pygame.draw.rect(output, self.color, self.lower)

    def get_sprites(self):
        return self.group.sprites()
