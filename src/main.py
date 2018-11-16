import pygame
from pygame.locals import *
import numpy as np
from copy import deepcopy

W, H = 600, 300
HUD_H = 38
pygame.init()
screen = pygame.display.set_mode((W, H+HUD_H), DOUBLEBUF)
screen.set_alpha(None)
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

BG_COLOR = (30, 30, 30)
PLAYER_COLOR = (200, 200, 200)
BLOCK_COLOR = (200, 10, 10)
TEST_COLOR = (10, 200, 80)
SPEED = .2
BOOST = 1
MIN_DIST = 250

class Bird(pygame.sprite.Sprite):
    def __init__(self, radius=round(H/30)):
        pygame.sprite.Sprite.__init__(self)
        self.x = W/4
        self.y = np.random.randint(30, H-30)
        self.vx = 0
        self.vy = 0
        # self.ax = 0
        # self.ay = 0
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
        self.dist = obstacle.x - self.x
        self.height = obstacle.y - self.y

    def draw_features(self, output):
        pygame.draw.line(output, TEST_COLOR, (self.x, self.y), (obstacle.x, self.y), 3)
        pygame.draw.line(output, TEST_COLOR, (self.x, self.y), (self.x, obstacle.y), 3)


class Block(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect

class Obstacle(object):
    # TODO: kill block when out of the screen

    def __init__(self, w=round(H/10), h=round(H/3), margin=round(H/10)):
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

    def update(self, dt, speed):
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

# bird = Bird()
birds = []
for i in range(20):
    birds.append(Bird())
valid_birds = deepcopy(birds)

obstacles = []
obstacles.append(Obstacle())

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

    c += 1

    score_surface = myfont.render("Score: {}".format(c), True, (0, 0, 0))

    if pygame.key.get_pressed()[pygame.K_SPACE]:
        for bird in valid_birds:
            bird.jump()

    for bird in valid_birds:
        bird.update(dt)

    obstacles_sprites = pygame.sprite.Group()
    for obstacle in obstacles:
        obstacles_sprites.add(obstacle.get_sprites())

    valid_birds[:] = [bird for bird in valid_birds if not (pygame.sprite.spritecollide(bird, obstacles_sprites, 0) or \
                      bird.y > H or bird.y < 0)]
    if len(valid_birds) == 0:
        if c > best_score:
            f = open(score_filename, "w")
            f.write(str(c))
            f.close()
            best_score = c
            best_score_surface = myfont.render("Best: {}".format(best_score),
                                               True, (0, 0, 0))
        c = 0
        speed = SPEED
        obstacles = []
        obstacles.append(Obstacle())
        valid_birds = deepcopy(birds)
        for bird in valid_birds:
            bird.__init__()
        pygame.time.wait(1000)
        clock = pygame.time.Clock()

    # for bird in birds:
    #     if pygame.sprite.spritecollide(bird, obstacles_sprites, 0) or \
    #        bird.y > H or bird.y < 0:
            # screen.fill(TEST_COLOR)
            # if c > best_score:
            #     f = open(score_filename, "w")
            #     f.write(str(c))
            #     f.close()
            #     best_score = c
            #     best_score_surface = myfont.render("Best: {}".format(best_score),
            #                                        True, (0, 0, 0))
            # c = 0
            # speed = SPEED
            # obstacles = []
            # obstacles.append(Obstacle())
            # bird.__init__()
            # pygame.time.wait(1000)
            # clock = pygame.time.Clock()

    if obstacles[0].x < 0-obstacles[0].w:
        del(obstacles[0])

    if obstacles[-1].last and obstacles[-1].x < W-MIN_DIST:
        obstacles[-1].last = False
        obstacles.append(Obstacle())

    for obstacle in obstacles:
        obstacle.update(dt, speed)
        obstacle.draw(screen)

    for bird in valid_birds:
        bird.draw(screen)
        next_obstacle = None
        for obstacle in obstacles:
            if obstacle.x > bird.x:
                next_obstacle = obstacle
                break
        if not next_obstacle is None:
            bird.get_features(next_obstacle)
            bird.draw_features(screen)

    pygame.draw.rect(screen, (255, 255, 255), hud_background)

    screen.blit(score_surface, (2,H))
    screen.blit(best_score_surface, (2,H+20))
    fps_surface = myfont.render("FPS: {:.0f}".format(clock.get_fps()),
                                True, (0, 0, 0))
    screen.blit(fps_surface, (W-65,H))

    pygame.display.flip()
