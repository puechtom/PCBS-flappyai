import pygame
from pygame.locals import *
from constant import *
import numpy as np
from keras.models import Sequential
from keras.layers import Dense

# predictions = model.predict(data)

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
        self.alive = True
        self.score = 0
        self.obstaclex = 0
        self.obstacley = 0
        self.model = Sequential()
        self.model.add(Dense(12,
                             input_dim=2,
                             kernel_initializer='uniform',
                             activation='relu'))
        # self.model.add(Dense(8,kernel_initializer='uniform',activation='relu'))
        self.model.add(Dense(1,kernel_initializer='uniform',activation='sigmoid'))
        self.model.compile(optimizer='rmsprop',
                           loss='binary_crossentropy',
                           metrics=['accuracy'])

    def fitness(self):
        pass

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
        self.obstaclex = obstacle.x+obstacle.w/2
        self.obstacley = obstacle.y
        self.dist = self.obstaclex - self.x
        self.height = self.obstacley - self.y
        return np.array([self.dist, self.height]).reshape((1,2))

    def draw_features(self, output):
        pygame.draw.line(output, TEST_COLOR, (self.x, self.y), (self.obstaclex, self.y), 3)
        pygame.draw.line(output, TEST_COLOR, (self.x, self.y), (self.x, self.obstacley), 3)

    def draw_goal(self, output):
        pygame.draw.circle(output, TEST_COLOR, (round(self.obstaclex), round(self.obstacley)), 3)
