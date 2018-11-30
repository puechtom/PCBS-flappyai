import pygame
from pygame.locals import *
from constant import *
import numpy as np
from obstacle import Obstacle
from bird import Bird

class World(object):
    def __init__(self, birds):
        self.birds = birds
        self.obstacles = []
        self.add_obstacle()

    def add_obstacle(self):
        self.obstacles.append(Obstacle())

    def update_obstacles(self, dt):
        create_obstacle = True
        for obstacle in self.obstacles:
            if create_obstacle and obstacle.x > W-MIN_DIST:
                create_obstacle = False
            obstacle.update(dt)
            if obstacle.x < 0-obstacle.w:
                del(obstacle)
        if create_obstacle:
            self.add_obstacle()

    def update_birds(self, dt):
        birds_alive = [bird for bird in self.birds if bird.alive]
        for bird in birds_alive:
            bird.update(dt)
            next_obstacle = None
            for obstacle in self.obstacles:
                if obstacle.x > bird.x:
                    next_obstacle = obstacle
                    break
            if not next_obstacle is None:
                bird.get_features(next_obstacle)

    def check_collisions(self):
        obstacles_sprites = pygame.sprite.Group()
        for obstacle in self.obstacles:
            obstacles_sprites.add(obstacle.get_sprites())
        birds_alive = [bird for bird in self.birds if bird.alive]
        for bird in birds_alive:
            if bird.alive:
                if pygame.sprite.spritecollide(bird, obstacles_sprites, 0) or \
                   bird.y > H or bird.y < 0:
                    bird.alive = False

    def update(self, dt):
        self.update_obstacles(dt)
        self.update_birds(dt)
        self.check_collisions()

    def draw_obstacles(self, output):
        for obstacle in self.obstacles:
            obstacle.draw(output)

    def draw_birds(self, output):
        birds_alive = [bird for bird in self.birds if bird.alive]
        for bird in birds_alive:
            bird.draw(output)
            # bird.draw_features(output)
            # bird.draw_goal(output)

    def draw(self, output):
        self.draw_obstacles(output)
        self.draw_birds(output)
