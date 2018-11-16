import pygame
from pygame.locals import *
from constant import *
import numpy as np

class Bird(pygame.sprite.Sprite):
    def __init__(self, radius=round(H/30)):
        pygame.sprite.Sprite.__init__(self)
        self.x = W/4
        self.y = np.random.randint(30, H-30)
        self.vx = 0
        self.vy = 0
        self.radius = radius
        self.score = 0
        self.color = (np.random.randint(50, 255),
                      np.random.randint(50, 255),
                      np.random.randint(50, 255))
        self.maxvy = .3
        self.rect = pygame.Rect(self.x-self.radius,
                                self.y-self.radius,
                                self.radius,
                                self.radius)

    def jump(self, jump_speed=.2):
        self.vy -= jump_speed
        if self.vy <= self.maxvy:
            self.vy = -self.maxvy

    def update(self, dt, g=.03):
        if abs(self.vy) <= self.maxvy:
            self.vy += g
        self.y += self.vy * dt * BOOST
        self.y = round(self.y)

    def draw(self, output):
        self.rect = pygame.Rect(self.x-self.radius,
                                self.y-self.radius,
                                self.radius,
                                self.radius)
        pygame.draw.circle(output, self.color, (round(self.x), round(self.y)), self.radius)

    def get_features(self, obstacle):
        self.obstaclex = obstacle.x
        self.obstacley = obstacle.y
        self.dist = self.obstaclex - self.x
        self.height = self.obstacley - self.y

    def draw_features(self, output):
        pygame.draw.line(output, TEST_COLOR, (self.x, self.y), (self.obstaclex, self.y), 3)
        pygame.draw.line(output, TEST_COLOR, (self.x, self.y), (self.x, self.obstacley), 3)
